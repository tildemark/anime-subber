# ========================================
# AnimeSubber GUI - CLI Usage Examples
# ========================================
# This script demonstrates various ways to use
# the main_app.py in CLI mode for automation.

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  AnimeSubber - CLI Examples" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# ========================================
# Example 1: Single File (High Quality)
# ========================================
Write-Host "Example 1: Single File - High Quality" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Command:" -ForegroundColor White
Write-Host 'python main_app.py --input "movie.mp4" --device cuda --resolution source --preset 6' -ForegroundColor Green
Write-Host "`nDescription:" -ForegroundColor White
Write-Host "  • Processes one file: movie.mp4" -ForegroundColor Gray
Write-Host "  • Uses GPU (CUDA) for AI subtitles" -ForegroundColor Gray
Write-Host "  • Keeps original resolution (source)" -ForegroundColor Gray
Write-Host "  • Best quality preset (6)" -ForegroundColor Gray
Write-Host "  • Time: ~40-80 hours for 2-hour movie`n" -ForegroundColor Gray

# ========================================
# Example 2: Single File (Fast)
# ========================================
Write-Host "Example 2: Single File - Fast Processing" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Command:" -ForegroundColor White
Write-Host 'python main_app.py --input "movie.mp4" --device cuda --resolution 720 --preset 10' -ForegroundColor Green
Write-Host "`nDescription:" -ForegroundColor White
Write-Host "  • Downscales to 720p (smaller file)" -ForegroundColor Gray
Write-Host "  • Fast preset (10)" -ForegroundColor Gray
Write-Host "  • Time: ~15-30 hours for 2-hour movie`n" -ForegroundColor Gray

# ========================================
# Example 3: Batch Folder
# ========================================
Write-Host "Example 3: Batch Folder Processing" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Command:" -ForegroundColor White
Write-Host 'python main_app.py --batch-folder "C:\Videos\Anime Season 1" --device cuda --resolution 1080 --preset 8' -ForegroundColor Green
Write-Host "`nDescription:" -ForegroundColor White
Write-Host "  • Processes ALL videos in folder" -ForegroundColor Gray
Write-Host "  • Auto-detects: .mp4, .mkv, .avi, .mov" -ForegroundColor Gray
Write-Host "  • 1080p resolution" -ForegroundColor Gray
Write-Host "  • Balanced preset (8)" -ForegroundColor Gray
Write-Host "  • Processes files sequentially`n" -ForegroundColor Gray

# ========================================
# Example 4: Batch with Auto-Shutdown
# ========================================
Write-Host "Example 4: Batch + Auto-Shutdown" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Command:" -ForegroundColor White
Write-Host 'python main_app.py --batch-folder "D:\Anime" --device cuda --resolution 1080 --preset 6 --shutdown' -ForegroundColor Green
Write-Host "`nDescription:" -ForegroundColor White
Write-Host "  • Processes entire folder" -ForegroundColor Gray
Write-Host "  • Shuts down PC after ALL files complete" -ForegroundColor Gray
Write-Host "  • Perfect for overnight processing" -ForegroundColor Gray
Write-Host "  • 60-second delay before shutdown`n" -ForegroundColor Gray

# ========================================
# Example 5: CPU Mode (No GPU)
# ========================================
Write-Host "Example 5: CPU Mode (No GPU Required)" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Command:" -ForegroundColor White
Write-Host 'python main_app.py --input "movie.mp4" --device cpu --resolution 720 --preset 8' -ForegroundColor Green
Write-Host "`nDescription:" -ForegroundColor White
Write-Host "  • Uses CPU for AI (no GPU needed)" -ForegroundColor Gray
Write-Host "  • Slower subtitle generation" -ForegroundColor Gray
Write-Host "  • Works on any PC`n" -ForegroundColor Gray

# ========================================
# Example 6: Quick Test
# ========================================
Write-Host "Example 6: Quick Test (Fastest Settings)" -ForegroundColor Yellow
Write-Host "---------------------------------------" -ForegroundColor Gray
Write-Host "Command:" -ForegroundColor White
Write-Host 'python main_app.py --input "test_clip.mp4" --device cpu --resolution 720 --preset 13' -ForegroundColor Green
Write-Host "`nDescription:" -ForegroundColor White
Write-Host "  • Fastest possible settings" -ForegroundColor Gray
Write-Host "  • Use for testing/debugging" -ForegroundColor Gray
Write-Host "  • Lower quality output`n" -ForegroundColor Gray

# ========================================
# Automation Script Example
# ========================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Automation Script Example" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "You can create a custom automation script:`n" -ForegroundColor White

$scriptExample = @'
# process_anime.ps1
# Automated anime processing script

$animeFolder = "D:\Downloads\Anime"
$device = "cuda"
$resolution = "1080"
$preset = "6"

# Process all videos in folder
python main_app.py `
    --batch-folder $animeFolder `
    --device $device `
    --resolution $resolution `
    --preset $preset `
    --shutdown

Write-Host "Processing started! PC will shutdown when complete."
'@

Write-Host $scriptExample -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Advanced: Scheduled Task" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "You can schedule automatic processing using Windows Task Scheduler:`n" -ForegroundColor White

Write-Host "1. Create a .ps1 script with your desired command" -ForegroundColor Gray
Write-Host "2. Open Task Scheduler" -ForegroundColor Gray
Write-Host "3. Create new task:" -ForegroundColor Gray
Write-Host "   • Trigger: Daily at 2:00 AM" -ForegroundColor Gray
Write-Host "   • Action: Run PowerShell script" -ForegroundColor Gray
Write-Host "   • Settings: Enable --shutdown flag" -ForegroundColor Gray
Write-Host "4. PC will auto-process new videos every night!`n" -ForegroundColor Gray

# ========================================
# Help
# ========================================
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Get Help" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "To see all available options:" -ForegroundColor White
Write-Host "python main_app.py --help`n" -ForegroundColor Green

Write-Host "For GUI mode (no arguments):" -ForegroundColor White
Write-Host "python main_app.py`n" -ForegroundColor Green

Write-Host "Documentation:" -ForegroundColor White
Write-Host "  • QUICKSTART_GUI.md - Quick start guide" -ForegroundColor Gray
Write-Host "  • GUI_README.md - Full documentation" -ForegroundColor Gray
Write-Host "  • README.md - Original CLI documentation`n" -ForegroundColor Gray

Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
