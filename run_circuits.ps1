$script = "circuit.py"
$qasm_file = "P3_sharp_peak.qasm"

$params = @(
    @{ p_frac = "0.9"; n_max = "0" }
    @{ p_frac = "0.91"; n_max = "0" }
    @{ p_frac = "0.92"; n_max = "0" }
    @{ p_frac = "0.93"; n_max = "0" }
    @{ p_frac = "0.94"; n_max = "0" }
    @{ p_frac = "0.95"; n_max = "0" }
    @{ p_frac = "0.96"; n_max = "0" }
    @{ p_frac = "0.97"; n_max = "0" }
    @{ p_frac = "0.98"; n_max = "0" }
    @{ p_frac = "0.99"; n_max = "0" }
    @{ p_frac = "0.991"; n_max = "0" }
    @{ p_frac = "0.992"; n_max = "0" }
    @{ p_frac = "0.993"; n_max = "0" }
    @{ p_frac = "0.994"; n_max = "0" }
    @{ p_frac = "0.995"; n_max = "0" }
    @{ p_frac = "0.996"; n_max = "0" }
    @{ p_frac = "0.997"; n_max = "0" }
    @{ p_frac = "0.998"; n_max = "0" }
    @{ p_frac = "0.999"; n_max = "0" }
    @{ p_frac = "1"; n_max = "2**5" }
    @{ p_frac = "1"; n_max = "2**6" }
    @{ p_frac = "1"; n_max = "2**7" }
    @{ p_frac = "1"; n_max = "2**8" }
    @{ p_frac = "1"; n_max = "2**9" }
    @{ p_frac = "1"; n_max = "2**10" }
    @{ p_frac = "1"; n_max = "2**11" }
    @{ p_frac = "1"; n_max = "2**12" }
    @{ p_frac = "1"; n_max = "2**13" }
    @{ p_frac = "1"; n_max = "2**14" }
    @{ p_frac = "1"; n_max = "2**15" }
    @{ p_frac = "1"; n_max = "2**16" }
    @{ p_frac = "1"; n_max = "2**17" }
    @{ p_frac = "1"; n_max = "2**18" }
    @{ p_frac = "1"; n_max = "2**19" }
    @{ p_frac = "1"; n_max = "2**20" }
    @{ p_frac = "1"; n_max = "2**21" }
    @{ p_frac = "1"; n_max = "2**22" }
    @{ p_frac = "1"; n_max = "2**23" }
    @{ p_frac = "1"; n_max = "2**24" }
    @{ p_frac = "1"; n_max = "2**25" }
    @{ p_frac = "1"; n_max = "2**26" }
    @{ p_frac = "1"; n_max = "2**27" }
    @{ p_frac = "1"; n_max = "2**28" }
    @{ p_frac = "1"; n_max = "2**29" }
)

function Get-PowFromString {
    param([string]$expr)
    $parts = $expr -split '\*\*'
    if ($parts.Count -ne 2) { return $expr }
    $base = [int]$parts[0]
    $exp  = [int]$parts[1]
    return [math]::Pow($base, $exp)
}

foreach ($param in $params) {
    $p_frac = $param.p_frac
    $n_max = [int](Get-PowFromString $param.n_max)
    $out_file = "out_gpu/out_$($p_frac)_$($n_max).txt"
    
    $cmd = "python $script $qasm_file $p_frac $n_max *> $out_file"
    Write-Host $cmd
    Invoke-Expression $cmd
}