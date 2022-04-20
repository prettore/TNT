##################################################
## Project: main data analysis
## Script purpose: extract and processing
## mobility/network features,  and show plots
## Date: 13/08/2020
## Author: Paulo H. L. Rettore
##################################################


# STEP: 0 -----------------------------------------------------------------
## load paths, input data, and libraries

# ipak function: install and load multiple R packages.
# check to see if packages are installed. Install them if they are not, then load them into the R session.
ipak <- function(pkg){
  new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
  if (length(new.pkg)) 
    install.packages(new.pkg, dependencies = TRUE)
  sapply(pkg, require, character.only = TRUE)
}

#library declarations
ipak(c('dplyr', 'ggplot2', 'ggmap','tm','tidytext','wordcloud','RColorBrewer','reshape2', 'maptools' ,
       "lubridate","igraph", "rgdal","spdep", "rgeos","markovchain","scales","plyr","gridExtra","tidyr","broom",
       "gstat","sp","spacetime","raster","ggrepel","doBy","TTR"))

#folder_proj <- gsub("data_analysis", "", getwd())  #Get main folder
folder_proj <- getwd()  #Get main folder


# STEP: 1 Trace Analysis --------------------------------------------------

#source("trace_data_analysis(markov).R")
#source("trace_data_analysis(bonnmotion).R")



# STEP: 2 Data Flow Analysis ----------------------------------------------

#source("D_ITG_data_analysis.R")

#source("emu_ip_packets_data_analysis(markov).R")
#source("emu_ip_packets_data_analysis(bonnmotion).R")

#source("tb_ip_packets_data_analysis(markov).R")
#source("tb_ip_packets_data_analysis(bonnmotion).R")

#source("emu_tb_ip_packets_data_analysis(stable).R")




