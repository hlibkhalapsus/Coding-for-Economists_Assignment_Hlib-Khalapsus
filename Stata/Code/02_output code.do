import delimited "$CLEAN\hotels-vienna-clean", bindquote(strict) varnames(1) encoding(UTF-8) clear

//Create summary statistics of price and distance sorting by stars
tabstat price, by(stars) statistics(mean median min max sd skew n)
tabstat distance, by(stars) statistics(mean median min max sd skew n)

//Create histograms and save them as files
hist price, by(stars) percent width(20) normal title ("Price Distribution") xtitle ("Price (US Dollars)")
graph export "$OUTPUT\hist_price.png", replace

hist distance, by(stars) percent normal title("Distance Distribution") xtitle ("Distance (Miles)")
graph export "$OUTPUT\hist_distance.png", replace

