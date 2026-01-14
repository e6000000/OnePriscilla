@echo off
rem ============================================================================
rem   GIT INDEX REFRESH (Variant 1: Reset & Clean)
rem   Ensures the git index is perfectly synced with .gitignore
rem   Usage: Call this script before 'git commit' or 'git push'
rem ============================================================================

echo [GIT-REFRESH] Cleaning index based on .gitignore...

rem 1. Remove everything from the index (files stay on disk)
rem    >nul 2>&1 hides output/errors if index is empty
git rm -r --cached . >nul 2>&1

rem 2. Add everything back
rem    Git will automatically respect the current .gitignore
git add .

echo [GIT-REFRESH] Index synchronized.
exit /b 0
