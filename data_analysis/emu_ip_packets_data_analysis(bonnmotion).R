##################################################
## Project: ip packets data analysis
## Script purpose: processing the ip pckts results
## Date: 11/09/2020
## Author: Paulo H. L. Rettore
##################################################


# STEP: 0 -----------------------------------------------------------------
## load paths, input data, and libraries

# reading traces
trace_folder <- paste(folder_proj,'/data', sep = "")
trace_file_name = list.files(
  path = trace_folder,        # directory to search within
  pattern = "Trace_.*(ProbRandomWalk|Waypoint|Manhattan|Gauss).*csv$", # regex pattern, some explanation below -".*(1|2).*csv$",
  recursive = TRUE,          # search subdirectories
  full.names = FALSE          # return the full path
)
files_to_read = list.files(
  path = trace_folder,        # directory to search within
  pattern = "Trace_.*(ProbRandomWalk|Waypoint|Manhattan|Gauss).*csv$", # regex pattern, some explanation below
  recursive = TRUE,          # search subdirectories
  full.names = TRUE          # return the full path
)

trace_lst = lapply(files_to_read, read.csv)  # read all the matching files
for(i in 1:length(trace_lst)){
  print(gsub(".csv","",gsub("Trace_","", trace_file_name[i])))
  trace_lst[[i]]$experiment <- gsub(".csv","",gsub("Trace_","", trace_file_name[i]))
}

# reading summary
filter_ini <-"ip_statistics_"#""
filter_fin <-  "_100p_2s.csv$"#"$"
statistics_folder <- paste(folder_proj,'/data/statistics', sep = "")
summary_file_name = list.files(
  path = statistics_folder,        # directory to search within
  pattern = paste(filter_ini,filter_fin,sep = "(ProbRandomWalk|RandomWaypoint|Manhattan|Gauss).*"), # regex pattern, some explanation below
  recursive = TRUE,          # search subdirectories
  full.names = FALSE          # return the full path
)
files_to_read = list.files(
  path = statistics_folder,        # directory to search within
  pattern = paste(filter_ini,filter_fin,sep = "(ProbRandomWalk|RandomWaypoint|Manhattan|Gauss).*"), # regex pattern, some explanation below
  recursive = TRUE,          # search subdirectories
  full.names = TRUE          # return the full path
)

summary_lst = lapply(files_to_read, read.csv)  # read all the matching files
for(i in 1:length(summary_lst)){
  print(gsub(filter_ini,"",gsub(filter_fin,"", summary_file_name[i])))
  summary_lst[[i]]$Experiment <- gsub(filter_ini,"",gsub(filter_fin,"", summary_file_name[i]))
}

# reading metrics
filter_ini <-"ip_statistics_"#""
filter_fin <- "_100p_2s_metrics.csv$"#"$"
metrics_file_name = list.files(
  path = statistics_folder,        # directory to search within
  pattern = paste(filter_ini,filter_fin,sep = "(ProbRandomWalk|RandomWaypoint|Manhattan|Gauss).*"), # regex pattern, some explanation below
  recursive = TRUE,          # search subdirectories
  full.names = FALSE          # return the full path
)
files_to_read = list.files(
  path = statistics_folder,        # directory to search within
  pattern = paste(filter_ini,filter_fin,sep = "(ProbRandomWalk|RandomWaypoint|Manhattan|Gauss).*"), # regex pattern, some explanation below
  recursive = TRUE,          # search subdirectories
  full.names = TRUE          # return the full path
)

metrics_lst = lapply(files_to_read, read.csv)  # read all the matching files
for(i in 1:length(metrics_lst)){
  print(gsub(filter_ini,"",gsub(filter_fin,"", metrics_file_name[i])))
  metrics_lst[[i]]$Experiment <- gsub(filter_ini,"",gsub(filter_fin,"", metrics_file_name[i]))
}


# #DITG logs
# metrics <- rbind(metrics_lst[[1]],metrics_lst[[2]],metrics_lst[[3]])
# colnames(metrics) <- c("Time","Bitrate","Delay","Jitter","Packet_loss","Round","Experiment") 


#Packets logs
summay_results <- rbind(summary_lst[[1]],summary_lst[[2]],summary_lst[[3]],summary_lst[[4]])


#Packets logs
metrics <- rbind(metrics_lst[[1]],metrics_lst[[2]],metrics_lst[[3]],metrics_lst[[4]])
#colnames(metrics) <- c("Time","Bitrate","Delay","Jitter","Inter_packet_delay","Packet_loss","Round","Experiment")
colnames(metrics) <- c("Time","Bitrate","Delay","Jitter","Packet loss","Round","Experiment")
metrics$Time <- as.POSIXct(metrics$Time)
metrics$Bitrate <- metrics$Bitrate/1000 

state_sequence_ex <- rbind(trace_lst[[1]],trace_lst[[2]],trace_lst[[3]],trace_lst[[4]])
state_sequence_ex <- state_sequence_ex[which(state_sequence_ex$node==0),]
state_sequence_ex <- state_sequence_ex[,c(4,5,9)]
state_sequence_ex$Feature <- 'State'
state_sequence_ex$state <- as.numeric(as.character(factor(state_sequence_ex$state)))
colnames(state_sequence_ex) <- c("Time","Value","Experiment","Feature")



# STEP 1: functions -------------------------------------------------------

## source: http://www.cookbook-r.com/Manipulating_data/Summarizing_data/
## http://www.cookbook-r.com/Graphs/Plotting_means_and_error_bars_(ggplot2)/
## Summarizes data.
## Gives count, mean, standard deviation, standard error of the mean, and confidence 
## interval (default 95%).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   groupvars: a vector containing names of columns that contain grouping variables
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySE <- function(data=NULL, measurevar, groupvars=NULL, na.rm=FALSE, conf.interval=.95) {
  library(doBy)
  
  # New version of length which can handle NA's: if na.rm==T, don't count them
  length2 <- function (x, na.rm=FALSE) {
    if (na.rm) sum(!is.na(x))
    else       length(x)
  }
  
  # Collapse the data
  formula <- as.formula(paste(measurevar, paste(groupvars, collapse=" + "), sep=" ~ "))
  datac <- summaryBy(formula, data=data, FUN=c(length2,mean,sd), na.rm=na.rm)
  
  # Rename columns
  names(datac)[ names(datac) == paste(measurevar, ".mean",    sep="") ] <- "mean" #measurevar
  names(datac)[ names(datac) == paste(measurevar, ".sd",      sep="") ] <- "sd"
  names(datac)[ names(datac) == paste(measurevar, ".length2", sep="") ] <- "N"
  
  datac$se <- datac$sd / sqrt(datac$N)  # Calculate standard error of the mean
  
  # Confidence interval multiplier for standard error
  # Calculate t-statistic for confidence interval: 
  # e.g., if conf.interval is .95, use .975 (above/below), and use df=N-1
  ciMult <- qt(conf.interval/2 + .5, datac$N-1)
  datac$ci <- datac$se * ciMult
  
  datac$Feature <- measurevar
  
  return(datac)
}


## Norms the data within specified groups in a data frame; it normalizes each
## subject (identified by idvar) so that they have the same mean, within each group
## specified by betweenvars.
##   data: a data frame.
##   idvar: the name of a column that identifies each subject (or matched subjects)
##   measurevar: the name of a column that contains the variable to be summariezed
##   betweenvars: a vector containing names of columns that are between-subjects variables
##   na.rm: a boolean that indicates whether to ignore NA's
normDataWithin <- function(data=NULL, idvar, measurevar, betweenvars=NULL,
                           na.rm=FALSE, .drop=TRUE) {
  library(plyr)
  
  # Measure var on left, idvar + between vars on right of formula.
  data.subjMean <- ddply(data, c(idvar, betweenvars), .drop=.drop,
                         .fun = function(xx, col, na.rm) {
                           c(subjMean = mean(xx[,col], na.rm=na.rm))
                         },
                         measurevar,
                         na.rm
  )
  
  # Put the subject means with original data
  data <- merge(data, data.subjMean)
  
  # Get the normalized data in a new column
  measureNormedVar <- paste(measurevar, "_norm", sep="")
  data[,measureNormedVar] <- data[,measurevar] - data[,"subjMean"] +
    mean(data[,measurevar], na.rm=na.rm)
  
  # Remove this subject mean column
  data$subjMean <- NULL
  
  return(data)
}


## Summarizes data, handling within-subjects variables by removing inter-subject variability.
## It will still work if there are no within-S variables.
## Gives count, un-normed mean, normed mean (with same between-group mean),
##   standard deviation, standard error of the mean, and confidence interval.
## If there are within-subject variables, calculate adjusted values using method from Morey (2008).
##   data: a data frame.
##   measurevar: the name of a column that contains the variable to be summariezed
##   betweenvars: a vector containing names of columns that are between-subjects variables
##   withinvars: a vector containing names of columns that are within-subjects variables
##   idvar: the name of a column that identifies each subject (or matched subjects)
##   na.rm: a boolean that indicates whether to ignore NA's
##   conf.interval: the percent range of the confidence interval (default is 95%)
summarySEwithin <- function(data=NULL, measurevar, betweenvars=NULL, withinvars=NULL,
                            idvar=NULL, na.rm=FALSE, conf.interval=.95, .drop=TRUE) {
  
  # Ensure that the betweenvars and withinvars are factors
  factorvars <- vapply(data[, c(betweenvars, withinvars), drop=FALSE],
                       FUN=is.factor, FUN.VALUE=logical(1))
  
  if (!all(factorvars)) {
    nonfactorvars <- names(factorvars)[!factorvars]
    message("Automatically converting the following non-factors to factors: ",
            paste(nonfactorvars, collapse = ", "))
    data[nonfactorvars] <- lapply(data[nonfactorvars], factor)
  }
  
  # Get the means from the un-normed data
  datac <- summarySE(data, measurevar, groupvars=c(betweenvars, withinvars),
                     na.rm=na.rm, conf.interval=conf.interval, .drop=.drop)
  
  # Drop all the unused columns (these will be calculated with normed data)
  datac$sd <- NULL
  datac$se <- NULL
  datac$ci <- NULL
  
  # Norm each subject's data
  ndata <- normDataWithin(data, idvar, measurevar, betweenvars, na.rm, .drop=.drop)
  
  # This is the name of the new column
  measurevar_n <- paste(measurevar, "_norm", sep="")
  
  # Collapse the normed data - now we can treat between and within vars the same
  ndatac <- summarySE(ndata, measurevar_n, groupvars=c(betweenvars, withinvars),
                      na.rm=na.rm, conf.interval=conf.interval, .drop=.drop)
  
  # Apply correction from Morey (2008) to the standard error and confidence interval
  #  Get the product of the number of conditions of within-S variables
  nWithinGroups    <- prod(vapply(ndatac[,withinvars, drop=FALSE], FUN=nlevels,
                                  FUN.VALUE=numeric(1)))
  correctionFactor <- sqrt( nWithinGroups / (nWithinGroups-1) )
  
  # Apply the correction factor
  ndatac$sd <- ndatac$sd * correctionFactor
  ndatac$se <- ndatac$se * correctionFactor
  ndatac$ci <- ndatac$ci * correctionFactor
  
  # Combine the un-normed means with the normed results
  merge(datac, ndatac)
}

# moving average by experiment and rounds
movingAverage <- function(data, window, column_metrics) {
  
  #window = 1
  #data <- metrics
  df_splitted <- split(data,list(data$Experiment,data$Round))
  
  df_sma <- as.data.frame(matrix(nrow = 0, ncol = length(colnames(df_splitted[[1]]))))
  #colnames(df_sma) <- c("Time","Bitrate","Delay","Jitter","Packet_loss","Round","Experiment") 
  
  #i <-0 
  for(experiment in df_splitted){
    #print(i)
    experiment[is.na(experiment)] <- 0
    test <- apply(experiment[,column_metrics], 2, SMA, n=window)
    test <- as.data.frame(test)
    
    test$Time <- experiment$Time
    test$Experiment <- experiment$Experiment
    test$Round <- experiment$Round
    
    df_sma <- rbind(df_sma,test)
    #i<-i+1
  }
  
  return(df_sma)
}

# replacing datetime to a second sequence by experiment and rounds
replacing_time <- function(data) {
  
  df_splitted <- split(data,list(data$Experiment,data$Round))
  df_result <- as.data.frame(matrix(nrow = 0, ncol = length(colnames(df_splitted[[1]]))))
  
  #i <-0 
  for(experiment in df_splitted){
    experiment <-experiment[order(experiment$Time),] # sorting tby time
    
    time_total <- difftime(max(experiment$Time), min(experiment$Time), units = "secs")
    time_interval <- time_total/(nrow(experiment)-1)
    experiment$Time <- seq(0, as.double(time_total), as.double(time_interval))
    
    
    df_result <- rbind(df_result,experiment)
    #i<-i+1
  }
  
  return(df_result)
}

# transforming state sequence to shows together with metric plot
transformingStateSequence <- function(trace, experiments) {
  
  trace <- trace[,c("time","state")]
  trace <- trace[!is.na(trace$state),]
  trace$state <- as.numeric(trace$state)
  state_sequence_ex <- as.data.frame(matrix(nrow = 0, ncol = 4))
  colnames(state_sequence_ex) <- c("Time","Experiment","Feature","Value")
  for(exp in experiments){
    trace$Experiment <- exp
    trace$Feature <- 'Bitrate'
    state_sequence_ex <- rbind(state_sequence_ex,trace)
  }
  state_sequence_ex$Experiment = factor(state_sequence_ex$Experiment, levels=c('suddenly','smooth','suddenly_short','smooth_short'))
  
  return(state_sequence_ex)
  
}

# fuction to rename labels in data frame columns
rename_labels <-  function(df,column,raw_names,new_names){
  
  for(i in 1:length(raw_names)){
    df[,column] <- replace(df[,column], df[,column]==raw_names[i], new_names[i])
  }
  return(df)
}

# STEP 3: metrics analysis ------------------------------------------------

#metrics <- rename_labels(metrics,'Experiment',c("Markov","Markov_Filled","Markov_Filled_Shortest"),c("Markov (raw)","Filled","Shortest and Filled"))
#colnames(metrics) <- c("Time","Bitrate","Delay","Jitter","IPD","Packet loss","Round","Experiment")
colnames(metrics) <- c("Time","Data Rate\n(kbit/s)","Delay\n(sec)","Jitter\n(sec)","Packet\nLoss (count)","Round","Experiment")


metrics_new_time <- replacing_time(metrics)



#metrics_sma <- movingAverage(metrics_new_time,5,c('Bitrate','Delay','Jitter','Packet loss'))
metrics_sma <- metrics_new_time


metrics_sma$Round <- NULL



df_metrics <- melt(metrics_sma, id.vars = c("Time","Experiment"))
colnames(df_metrics) <- c("Time","Experiment","Feature","Value") 
#df_metrics <- rbind(df_metrics,state_sequence_ex)
#df_metrics$Feature = factor(df_metrics$Feature, levels=c('State','Bitrate','Delay','IPD','Jitter','Packet loss'))
df_metrics$Feature = factor(df_metrics$Feature, levels=c("Data Rate\n(kbit/s)","Packet\nLoss (count)","Delay\n(sec)","Jitter\n(sec)"))


# x axis treated as continuous variable
p <- ggplot(data=df_metrics, aes(x=Time, y=Value, color=Feature,fill=Experiment)) +
  geom_line(aes(linetype=Feature),size=.4,alpha = .3) + geom_point(aes(shape = Experiment),size=.8,alpha =0.8)+
  geom_smooth(span = 0.28,linetype="dashed",color="red",size=0.5,fill="red",alpha=0.3, se=TRUE) +
  #scale_color_brewer(palette="Pal_grau")+
  #scale_fill_grey(start = 1, end = 0.3) +
  scale_color_grey(start = 0.6, end = .1) +
  #scale_x_continuous(breaks= seq(0, max(df_metrics$Time), by=60)) +
  theme_minimal() + 
  theme(axis.text=element_text(size=10),
        axis.title=element_text(size=10),legend.title=element_text(size=10), axis.text.x = element_text(angle = 45),
        legend.text=element_text(size=10),strip.text.x = element_text(size = 10),legend.position = "none") +
  facet_grid(Feature~Experiment, scales = "free")  
#geom_step(data=state_sequence_ex, aes(x=time, y=state),color='black',linetype = "dashed")
#facet_wrap(~Metrics, scales = "free",ncol = 2)

plot(p)

