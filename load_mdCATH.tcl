proc load_mdCATH {fn temperature replica} { 
	set tmp [exec h5ls $fn]
	set code [lindex $tmp 0]
	set tmpdir $::env(TMPDIR)
	set pdbname $tmpdir/loadmdcath.pdb 
	exec h5dump -b -o $pdbname -d /$code/pdbProteinAtoms $fn
	set cbin $tmpdir/coords.bin
	exec h5dump -b -o $cbin -d /$code/sims${temperature}K/$replica/coords $fn

	mol new $pdbname
	set N [molinfo top get numatoms]
	animate delete all

	set fp [open $cbin r]
	fconfigure $fp -translation binary
	set cdat [read $fp]
	close $fp

	set M [binary scan $cdat f* dat]

	return $dat
}
