import os, subprocess, filecmp

def test_StdToVineConversion():
    # First, run the converter.
    cmd = "python stdPhylogeny2vine.py -path tests/ -file test-data.json -verbose -parentTrait fitness -traits trait1 trait2 fitness"
    subprocess.run(cmd, shell=True)
    # Next, check that generated vineData directories matches expected
    assert os.path.isdir("vineData/snapshots/snapshot_gen_0000")
    assert os.path.isdir("vineData/snapshots/snapshot_gen_0001")
    assert os.path.isdir("vineData/snapshots/snapshot_gen_0002")
    assert os.path.isdir("vineData/snapshots/snapshot_gen_0003")
    assert os.path.isdir("vineData/snapshots/snapshot_gen_0004")
    # Compare generated vineData to expected-vineData
    dirs = os.listdir("vineData/snapshots")
    for d in dirs:
        expected_d = os.path.join("tests", "expected-vineData", "snapshots", d)
        generated_d = os.path.join("vineData", "snapshots", d)
        expected_files = os.listdir(expected_d)
        generated_files = os.listdir(generated_d)
        # Check that files match up
        assert expected_files == generated_files
        for fname in expected_files:
            expected_f = os.path.join(expected_d, fname)
            generated_f = os.path.join(generated_d, fname)
            assert filecmp.cmp(expected_f, generated_f)