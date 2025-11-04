// Set relative paths
cd "C:\Users\Khalapsus_Hlib\Downloads\Coding for Economists_Assignment_Hlib Khalapsus\Stata"
local PROJDIR "`c(pwd)'"

// Use globals to set paths for each of the folders 
global RAW "`PROJDIR'\Data\Raw"
global CLEAN "`PROJDIR'\Data\Clean"
global CODE "`PROJDIR'\Code"
global OUTPUT "`PROJDIR'\Output"

// Execute the do files
do "$CODE\01_clean data.do"
do "$CODE\02_output code.do"

