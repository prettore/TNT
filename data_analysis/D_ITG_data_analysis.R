##################################################
## Project: D-ITG data analysis
## Script purpose: processing the ITG results
## Date: 17/07/2020
## Author: Paulo H. L. Rettore
##################################################


# STEP: 0 -----------------------------------------------------------------
## load paths, input data, and libraries


trace_GaussMarkov <- read.csv(paste(folder_proj,"/data/Trace_GaussMarkov.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading state pattern
GaussMarkov_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_GaussMarkov_300p_10kbps_128kb_2s.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
GaussMarkov_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_GaussMarkov_300p_10kbps_128kb_2s_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
GaussMarkov_motion$Experiment <- 'GaussMarkov'
GaussMarkov_motion_metrics$Experiment <- 'GaussMarkov'
trace_GaussMarkov$Experiment <- 'GaussMarkov'

trace_Boundless <- read.csv(paste(folder_proj,"/data/Trace_Boundless.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading state pattern
Boundless_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_Boundless_300p_10kbps_128kb_2s.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
Boundless_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_Boundless_300p_10kbps_128kb_2s_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
Boundless_motion$Experiment <- 'Boundless'
Boundless_motion_metrics$Experiment <- 'Boundless'
trace_Boundless$Experiment <- 'Boundless'

trace_ManhattanGrid <- read.csv(paste(folder_proj,"/data/Trace_ManhattanGrid.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading state pattern
ManhattanGrid_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_ManhattanGrid_300p_10kbps_128kb_2s.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
ManhattanGrid_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_ManhattanGrid_300p_10kbps_128kb_2s_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
ManhattanGrid_motion$Experiment <- 'ManhattanGrid'
ManhattanGrid_motion_metrics$Experiment <- 'ManhattanGrid'
trace_ManhattanGrid$Experiment <- 'ManhattanGrid'

trace_RandomWalk <- read.csv(paste(folder_proj,"/data/Trace_RandomWalk.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading state pattern
RandomWalk_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_RandomWalk_300p_10kbps_128kb_2s.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
RandomWalk_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_RandomWalk_300p_10kbps_128kb_2s_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
RandomWalk_motion$Experiment <- 'RandomWalk'
RandomWalk_motion_metrics$Experiment <- 'RandomWalk'
trace_RandomWalk$Experiment <- 'RandomWalk'


experiments_data <- rbind(GaussMarkov_motion[,c(5:18)],Boundless_motion[,c(5:18)],ManhattanGrid_motion[,c(5:18)],RandomWalk_motion[,c(5:18)])
experiments_data$bytes_received <- experiments_data$bytes_received/1024

metrics <- rbind(GaussMarkov_motion_metrics,Boundless_motion_metrics,ManhattanGrid_motion_metrics,RandomWalk_motion_metrics)
colnames(metrics) <- c("Time","Bitrate","Delay","Jintter","Packet_loss","Round","Experiment")

state_sequence_ex <- rbind(trace_GaussMarkov[which(trace_GaussMarkov$node==0),],trace_Boundless[which(trace_Boundless$node==0),],
                           trace_ManhattanGrid[which(trace_ManhattanGrid$node==0),],trace_RandomWalk[which(trace_RandomWalk$node==0),])
state_sequence_ex <- state_sequence_ex[,c(2,5,10)]
state_sequence_ex$Feature <- 'State'
state_sequence_ex$state <- as.numeric(state_sequence_ex$state)
colnames(state_sequence_ex) <- c("Time","Value","Experiment","Feature")

# suddenly_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_400pcts.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# suddenly_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_400pcts_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# smooth_short_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_smooth_short_400pcts.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# smooth_short_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_smooth_short_400pcts_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# suddenly_short_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_short_400pcts.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# suddenly_short_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_short_400pcts_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# #
# smooth_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_smooth_400pcts_2k.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# smooth_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_smooth_400pcts_2k_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# suddenly_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_400pcts_2k.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# suddenly_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_400pcts_2k_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# smooth_short_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_smooth_short_400pcts_2k.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# smooth_short_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_smooth_short_400pcts_2k_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# suddenly_short_motion <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_short_400pcts_2k.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading summaring data
# suddenly_short_motion_metrics <- read.csv(paste(folder_proj,"/data/statistics/statistics_suddenly_short_400pcts_2k_metrics.csv", sep = ""),stringsAsFactors=FALSE, sep=",")  #reading metrics data
# 
# 
# smooth_short_motion$experiment <- 'smooth_short'
# suddenly_short_motion$experiment <- 'suddenly_short'
# smooth_motion$experiment <- 'smooth'
# suddenly_motion$experiment <- 'suddenly'
# experiments_data <- rbind(smooth_motion[,c(5:18)],suddenly_motion[,c(5:18)],smooth_short_motion[,c(5:18)],suddenly_short_motion[,c(5:18)])
# experiments_data$bytes_received <- experiments_data$bytes_received/1024
# 
# smooth_motion_metrics$experiment <- 'smooth'
# suddenly_motion_metrics$experiment <- 'suddenly'
# smooth_short_motion_metrics$experiment <- 'smooth_short'
# suddenly_short_motion_metrics$experiment <- 'suddenly_short'
#metrics <- rbind(smooth_motion_metrics,suddenly_motion_metrics,smooth_short_motion_metrics,suddenly_short_motion_metrics)


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
movingAverage <- function(data, window) {
  
  #window = 1
  #data <- metrics
  df_splitted <- split(data,list(data$Experiment,data$Round))
  
  df_sma <- as.data.frame(matrix(nrow = 0, ncol = length(colnames(df_splitted[[1]]))))
  colnames(df_sma) <- c("Time","Bitrate","Delay","Jintter","Packet_loss","Round","Experiment") 
  
  #i <-0 
  for(experiment in df_splitted){
    #print(i)
    test <- apply(experiment[,2:5], 2, SMA, n=window)
    test <- as.data.frame(test)
    
    test$Time <- experiment$Time
    test$Experiment <- experiment$Experiment
    test$Round <- experiment$Round
    
    df_sma <- rbind(df_sma,test)
    #i<-i+1
    }
  
  return(df_sma)
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


# STEP 2: summary analysis ------------------------------------------------
# summarySE provides the standard deviation, standard error of the mean, and a (default 95%) confidence interval
colnames(experiments_data) <- c("total_time_s", "packets_received","min_delay_s","max_delay_s","avg_delay_s",
                    "sd_delay_s","avg_jitter_s","bytes_received","avg_bitrate_kb","avg_packetrate_pkts",
                    "packet_dropped","packet_dropped_pct","avg_loss_burst_pkt","experiment")
                    
                    
                    
#summary_tt <- summarySE(experiments_data, measurevar="total_time_s", groupvars=c("experiment"))
summary_tp <- summarySE(experiments_data, measurevar="packets_received", groupvars=c("experiment"))
#summary_dlmin <- summarySE(experiments_data, measurevar="min_delay_s", groupvars=c("experiment"))
summary_dlmax <- summarySE(experiments_data, measurevar="max_delay_s", groupvars=c("experiment"))
summary_dl <- summarySE(experiments_data, measurevar="avg_delay_s", groupvars=c("experiment"))
summary_jt <- summarySE(experiments_data, measurevar="avg_jitter_s", groupvars=c("experiment"))
summary_br <- summarySE(experiments_data, measurevar="avg_bitrate_kb", groupvars=c("experiment"))
#summary_byt <- summarySE(experiments_data, measurevar="bytes_received", groupvars=c("experiment"))
#summary_pr <- summarySE(experiments_data, measurevar="avg_packetrate_pkts", groupvars=c("experiment"))
summary_pd <- summarySE(experiments_data, measurevar="packet_dropped", groupvars=c("experiment"))
#summary_pdp <- summarySE(experiments_data, measurevar="packet_dropped_pct", groupvars=c("experiment"))


summary_ex <- rbind(summary_tp,summary_dlmax,summary_dl,summary_jt,summary_br,summary_pd)
#summary_ex$experiment = factor(summary_ex$experiment, levels=c('suddenly','smooth','suddenly_short','smooth_short'))

p <- ggplot(summary_ex, aes(x=Feature, y=mean, fill=experiment)) + 
  geom_bar(position=position_dodge(), stat="identity",
           colour="black", # Use black outlines,
           size=.3) +      # Thinner lines
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se),
                size=.3,    # Thinner lines
                width=.2,
                position=position_dodge(.9)) +
  xlab("Metric") +
  ylab("Value") +
  scale_fill_brewer(palette="Paired") +
  #scale_fill_hue(name="Experiment", # Legend label, use darker colors
  #               breaks=c("smooth", "suddenly"),
  #               labels=c("Smooth", "Suddenly")) +
  ggtitle("The effect of Data Rate change using Mobility in Tactical Networks") +
  #scale_y_continuous(breaks=0:max(summary_ex$mean)*1) +
  theme_minimal() + facet_wrap(~Feature, scales = "free")

plot(p)

# The errorbars overlapped, so use position_dodge to move them horizontally
# pd <- position_dodge(0.1) # move them .05 to the left and right
# 
# ggplot(tgc2, aes(x=feature, y=mean, colour=experiment, group=experiment)) + 
#   geom_errorbar(aes(ymin=mean-se, ymax=mean+se), colour="black", width=.1, position=pd) +
#   geom_line(position=pd) +
#   geom_point(position=pd, size=3, shape=21, fill="white") + # 21 is filled circle
#   xlab("Metric") +
#   ylab("Value") +
#   scale_colour_hue(name="Experiment",    # Legend label, use darker colors
#                    breaks=c("smooth", "suddenly"),
#                    labels=c("Smooth", "Suddenly"),
#                    l=40) +                    # Use darker colors, lightness=40
#   ggtitle("The effect of Data Rate changing using Mobility in Tactical Networks") +
#   expand_limits(y=0) +                        # Expand y range
#   #scale_y_continuous(breaks=0:20*4) +         # Set tick every 4
#   theme_bw()  + facet_wrap(.~feature, scales = "free") +
#   theme(legend.justification=c(1,0),
#         legend.position=c(1,0))               # Position legend in bottom right


# STEP 3: metrics analysis ------------------------------------------------

 
# filter the df to show values greater then 0
#metrics <- filter(metrics, Bitrate > 0, Delay > 0)

metrics_sma <- movingAverage(metrics,1)


summary_br <- summarySE(metrics_sma, measurevar="Bitrate", groupvars=c("Time","Experiment"))
summary_dl <- summarySE(metrics_sma, measurevar="Delay", groupvars=c("Time","Experiment"))
summary_jt <- summarySE(metrics_sma, measurevar="Jintter", groupvars=c("Time","Experiment"))
summary_pd <- summarySE(metrics_sma, measurevar="Packet_loss", groupvars=c("Time","Experiment"))


summary_metrics <- rbind(summary_br,summary_dl,summary_jt,summary_pd)
#summary_metrics$Experiment = factor(summary_metrics$Experiment, levels=c('suddenly','smooth','suddenly_short','smooth_short'))


#state_sequence_ex <- transformingStateSequence(trace_node1,c('suddenly','smooth','suddenly_short','smooth_short'))
#state_sequence_ex <- transformingStateSequence(trace_node1[which(trace_node1$node==0),],'smooth')






df_metrics <- melt(metrics_sma[,1:6], id.vars = c("Time","Experiment"))
colnames(df_metrics) <- c("Time","Experiment","Feature","Value") 
df_metrics <- rbind(df_metrics,state_sequence_ex)
df_metrics$Feature = factor(df_metrics$Feature, levels=c('State','Bitrate','Delay','Jintter','Packet_loss'))

#df_metrics$Experiment = factor(df_metrics$Experiment, levels=c('suddenly','smooth','suddenly_short','smooth_short'))
# x axis treated as continuous variable
p <- ggplot(data=df_metrics, aes(x=Time, y=Value, color=Feature,fill=Experiment)) +
  geom_line(aes(linetype=Feature)) + geom_point(aes(shape = Experiment))+
  scale_color_brewer(palette="Paired")+
  scale_x_continuous(breaks= seq(0, max(df_metrics$Time), by=60)) +
  theme_minimal() + theme(legend.position = "none") + 
  facet_grid(Feature~Experiment, scales = "free")  
  #geom_step(data=state_sequence_ex, aes(x=time, y=state),color='black',linetype = "dashed")
  #facet_wrap(~Metrics, scales = "free",ncol = 2)

plot(p)


# The errorbars overlapped, so use position_dodge to move them horizontally
pd <- position_dodge(0.1) # move them .05 to the left and right
p <- ggplot(summary_metrics, aes(x=Time, y=mean, colour=Feature, group=Feature)) + 
  geom_errorbar(aes(ymin=mean-se, ymax=mean+se), colour="darkgray", width=.1, position=pd) +
  geom_line(position=pd) +
  geom_point(position=pd, size=1.5, shape=21, fill="white") + # 21 is filled circle
  xlab("Time") +
  ylab("Value") +
  #scale_colour_hue(name="Experiment",    # Legend label, use darker colors
  #                 breaks=c("suddenly", "smooth"),
  #                 labels=c("suddenly", "smooth"),
  #                 l=40) +                    # Use darker colors, lightness=40
  #ggtitle("The Effect of Vitamin C on\nTooth Growth in Guinea Pigs") +
  scale_x_continuous(breaks= seq(0, max(summary_metrics$Time), by=60)) +
  expand_limits(y=0) +                        # Expand y range
  #scale_y_continuous(breaks=0:20*4) +         # Set tick every 4
  theme_minimal() + theme(legend.position = "none") + #theme_bw() +
  #theme(legend.justification=c(1,0),
  #      legend.position=c(1,0))      +         # Position legend in bottom right
  facet_grid(Feature~Experiment, scales = "free") + 
  geom_step(data=state_sequence_ex, aes(x=Time, y=Value),color='black',linetype = "dashed")

plot(p)

