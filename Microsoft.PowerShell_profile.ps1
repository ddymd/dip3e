#oh-my-posh init pwsh --config "$(scoop prefix oh-my-posh)\themes\jandedobbeleer.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\powerlevel10k_lean.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\sorin.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\atomicBit.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\peru.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\kali.omp.json" | Invoke-Expression
oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\negligible.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\atomicBit.omp.json" | Invoke-Expression
#oh-my-posh init pwsh --config "$Env:POSH_THEMES_PATH\wopian.omp.json" | Invoke-Expression

Import-Module posh-git
Import-Module PSReadLine

Import-Module "C:\Program Files (x86)\Microsoft Visual Studio\2019\Professional\Common7\Tools\Microsoft.VisualStudio.DevShell.dll"
# Vs InstanceId get by "C:\Program Files (x86)\Microsoft Visual Studio\Installer\vswhere.exe"
Enter-VsDevShell -VsInstanceId 5fb759ba -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -no_logo'

Set-PSReadLineOption -PredictionSource History

#Set-PSReadLineOption -Colors @{ InlinePrediction = "$([char]0x1b)[38;5;238m"}
Set-PSReadLineOption -Colors @{ InlinePrediction = "$([char]0x1b)[36;7;238m"}

Set-PSReadLineOption -PredictionViewStyle InlineView
#Set-PSReadLineOption -PredictionViewStyle ListView

# Set-PSReadLineOption -EditMode Vi
Set-PSReadLineOption -EditMode Emacs

# function OnViModeChange {
#     if ($args[0] -eq 'Command') {
#         # Set the cursor to a blinking block.
#         Write-Host -NoNewLine "`e[1 q"
#     } else {
#         # Set the cursor to a blinking line.
#         Write-Host -NoNewLine "`e[5 q"
#     }
# }
# Set-PSReadLineOption -ViModeIndicator Script -ViModeChangeHandler $Function:OnViModeChange

# Set-PSReadLineOption -Colors @{
#   Command            = 'Magenta'
#   Number             = 'DarkGray'
#   Member             = 'DarkGray'
#   Operator           = 'DarkGray'
#   Type               = 'DarkGray'
#   Variable           = 'DarkGreen'
#   Parameter          = 'DarkGreen'
#   ContinuationPrompt = 'DarkGray'
#   Default            = 'DarkGray'
# }

Set-PSReadlineOption -BellStyle None

[System.Console]::OutputEncoding = [System.Text.Encoding]::GetEncoding("utf-8")
[System.Console]::InputEncoding = [System.Text.Encoding]::GetEncoding("utf-8")

$env:LESSCHARSET = "utf-8"

# 这边我们需要安装awk和fzf: scoop install gawk ,,,, scoop install fzf
Set-PSReadLineKeyHandler -Chord Ctrl+r -ScriptBlock {
	$command = Get-Content (Get-PSReadlineOption).HistorySavePath | awk '!a[$0]++' | fzf --tac
	[Microsoft.PowerShell.PSConsoleReadLine]::Insert($command)
}

#region conda initialize
# !! Contents within this block are managed by 'conda init' !!
# (& "C:\Users\Jack\scoop\apps\miniconda3\current\Scripts\conda.exe" "shell.powershell" "hook") | Out-String | Invoke-Expression
#endregion
