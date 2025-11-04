// Ensure a proper opening of the CSV file by omitting common data quality errors
import delimited "$RAW\hotels-vienna-raw", bindquote(strict) varnames(1) encoding(UTF-8) clear

// SORT THE DATA

// We keep only the variables that are essential for our analysis
keep hotel_id country city_actual distance price city stars accommodation_type 

// We only keep the observations that are located in Vienna and are hotels
keep if city_actual == "Vienna"
keep if accommodation_type == "Hotel"

// We only keep 3 and 4 star hotels
keep if stars >= 3 & stars <= 4

//In addition, we drop the outliers from the data
drop if price >= 1000
drop if distance >= 8

save "$CLEAN\hotels-vienna-clean.dta", replace
export delimited using "$CLEAN\hotels-vienna-clean.csv", replace