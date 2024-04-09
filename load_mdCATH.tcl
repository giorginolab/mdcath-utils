proc load_mdCATH {fn temperature replica} { 
    # Try to execute h5ls and handle errors
    set status [catch {exec h5ls $fn} tmp]
    if {$status} {
        return -code error "Error executing h5ls on file $fn: $tmp"
    }
    set code [lindex $tmp 0]

    set tmpdir $::env(TMPDIR)
    set pdbname $tmpdir/loadmdcath.pdb 

    # Handle potential errors from h5dump
    if {[catch {exec h5dump -b -o $pdbname -d /$code/pdbProteinAtoms $fn} result]} {
        return -code error "Error dumping pdbProteinAtoms from $fn: $result"
    }

    set cbin $tmpdir/coords.bin
    if {[catch {exec h5dump -b -o $cbin -d /$code/sims${temperature}K/$replica/coords $fn} result]} {
        return -code error "Error dumping coords from $fn: $result"
    }

    # Load the molecular data
    mol new $pdbname
    set N [molinfo top get numatoms]
    if {$N == 0} {
        return -code error "No atoms found in the molecule loaded from $pdbname"
    }
    animate delete all

    # Handle file opening and binary data reading
    if {[catch {open $cbin r} fp msg]} {
        return -code error "Error opening coordinates file $cbin: $msg"
    }
    fconfigure $fp -translation binary
    if {[catch {read $fp} cdat]} {
        close $fp
        return -code error "Error reading data from coordinates file $cbin"
    }
    close $fp

    # Binary data processing
    set M [binary scan $cdat f* dat]
    if {$M == 0} {
        return -code error "Failed to scan binary data from $cbin"
    }

    return $dat
}
