##################################################
## Project: trace analysis
## Script purpose: extract mobility features and
## show plots
## Date: 14/10/2020
## Author: Paulo H. L. Rettore
##################################################


# STEP: 0 -----------------------------------------------------------------
## load paths, input data, and libraries

# reading traces
trace_folder <- paste(folder_proj,'/data/vhf', sep = "")
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


traces <- rbind(trace_lst[[1]],trace_lst[[2]],trace_lst[[3]],trace_lst[[4]])
traces <- traces[which(traces$node==0),]
traces$state <- as.numeric(as.character(traces$state))
traces$time <- traces$time/60
traces$speed <- traces$speed * 3.6
traces$acc <- traces$acc * 3.6
traces$distance <- traces$distance/1000


# STEP 1: functions -------------------------------------------------------


# calculating data rate statistics
calculating_trace_statistics <- function(data_f) {
  
  
  #data_f <- traces
  
  #df_result <- as.data.frame(matrix(nrow = 0, ncol = length(colnames(df_splitted[[1]]))))
  
  data_f$DR <- mapvalues(data_f$state, from=c('0','1','2','3','4','5'), to=c('0','0.6','1.2','2.4','4.8','9.6'))
  data_f$DR <- as.numeric(data_f$DR)
  
  df_splitted <- split(data_f,list(data_f$experiment))
  for(set in df_splitted){
    cat("Experiment: ", head(set$experiment,n=1),"\n")
    cat("Data Rate Statistics\n")
    exp_time <- max(set$time) - min(set$time)
    mean_time <- sum(set$DR)/exp_time
    cat("Data rate (avg): ",mean_time) 
    sd_time <- sqrt(sum((set$DR-mean_time)^2/(exp_time)))
    cat(" Data rate (sd): ",sd_time,"\n") 
    
    cat("Statistics avoinding the experiment duration: ")
    cat("Data rate (avg): ",mean(set$DR))
    cat(" Data rate (sd): ",sd(set$DR),"\n\n")
    
    cat("Trace Statistics\n")
    cat("Distance (avg): ",mean(set$distance))
    cat(" Distance (max): ",max(set$distance),"\n")
    cat("Speed (avg): ",mean(set$speed))
    cat(" Speed (max): ",max(set$speed),"\n")
    cat("Acc (avg): ",mean(set$acc))
    cat(" Acc (max): ",max(set$acc),"\n\n")
    
    
    #df_result <- rbind(df_result,experiment)
  }
  
  #return(df_result)
}

# fuction to rename labels in data frame columns
rename_labels <-  function(df,column,raw_names,new_names){
  
  for(i in 1:length(raw_names)){
    df[,column] <- replace(df[,column], df[,column]==raw_names[i], new_names[i])
  }
  return(df)
}

# STEP 2: summary analysis ------------------------------------------------



calculating_trace_statistics(traces)


colnames(traces) <- c("Node","X","Y","Time","State","Distance (km)","Speed (km/h)","Acc (km/h2)","Experiment")
traces_melt <- melt(traces[,c(4:9)], id.vars = c("Time","Experiment"))
colnames(traces_melt) <- c("Time","Experiment","Feature","Value")
traces_melt$Value <- as.numeric(traces_melt$Value)

traces_melt <- rename_labels(traces_melt,'Experiment',c("GaussMarkov_VHF","ManhattanGrid_VHF","ProbRandomWalk_VHF","RandomWaypoint_VHF"),c("GM", "MG", "PRW","RWP"))
#traces_melt <- rename_labels(traces_melt,'Experiment',c("GaussMarkov","ManhattanGrid","ProbRandomWalk","RandomWaypoint"),c("GM", "MG", "PRW","RWP"))
traces_melt$Experiment = factor(traces_melt$Experiment, levels=c("GM", "MG", "PRW","RWP"))







# trace_experiment <- traces_melt %>% filter(Feature != "State")
# p <- ggplot(trace_experiment, aes(x=Feature, y=Value, fill=Experiment)) + 
#   geom_bar(position=position_dodge(), stat="identity",
#            colour="black", # Use black outlines,
#            size=.3) +      # Thinner lines
#   xlab("Metric") +
#   ylab("Value") +
#   scale_fill_brewer(palette="Paired") +
#   #scale_fill_hue(name="Experiment", # Legend label, use darker colors
#   #               breaks=c("smooth", "suddenly"),
#   #               labels=c("Smooth", "Suddenly")) +
#   #scale_y_continuous(breaks=0:max(summary_ex$mean)*1) +
#   theme_minimal() + facet_wrap(~Experiment, scales = "free")
# plot(p)

#traces_melt$Experiment = factor(traces_melt$Experiment, levels=c('suddenly','smooth','suddenly_short','smooth_short'))

state_color <- c('0' ='#CC0000', '1' ='#FFE66C', '2' ='#EBD367', '3' ='#D0B100', '4' ='#2B8C48', '5' ='#005E25')
trace_experiment <- traces_melt %>% filter(Feature == "State")
# x axis treated as continuous variable
p <- ggplot(data=trace_experiment, aes(x=Time, y=Value)) +
  geom_line(linetype="dashed",color="gray") + 
  geom_point(aes(shape = Experiment,color=as.factor(Value))) +
  #scale_color_brewer(palette="Pastel2")+
  scale_colour_manual(values = state_color) +
  theme_minimal() + 
  labs(x="Time in minutes")+
  theme(axis.text=element_text(size=10),
        axis.title=element_text(size=10),legend.title=element_text(size=10), 
        legend.text=element_text(size=10),strip.text.x = element_text(size = 10),legend.position = "none") +
  facet_wrap(~Experiment, ncol = 1)  
#geom_step(data=state_sequence_ex, aes(x=time, y=state),color='black',linetype = "dashed")
#facet_wrap(~Metrics, scales = "free",ncol = 2)
plot(p)

trace_experiment <- traces_melt %>% filter(Experiment == "GM")
# x axis treated as continuous variable
p <- ggplot(data=trace_experiment, aes(x=Time, y=Value, color=Feature,fill=Experiment)) +
  geom_line(aes(linetype=Feature)) + geom_point(aes(shape = Experiment))+
  scale_color_brewer(palette="Pastel2")+
  #scale_x_continuous(breaks= seq(0, max(df_metrics$Time), by=60)) +
  theme_minimal() + 
  labs(x="Time in minutes")+
  theme(axis.text=element_text(size=10),
        axis.title=element_text(size=10),legend.title=element_text(size=10), 
        legend.text=element_text(size=10),strip.text.x = element_text(size = 10),legend.position = "none") +
  facet_grid(Feature~Experiment, scales = "free")  
#geom_step(data=state_sequence_ex, aes(x=time, y=state),color='black',linetype = "dashed")
#facet_wrap(~Metrics, scales = "free",ncol = 2)
plot(p)


trace_experiment <- traces_melt %>% filter(Feature != "State")
p <- ggplot(data=trace_experiment, aes(x=Experiment, y=Value, fill=Experiment)) +
  geom_boxplot(width=0.3, outlier.size = .3)+
  # Edit legend title, labels and Gradient colors
  #scale_fill_brewer(palette="RdBu",name = "Trace", labels = c("Markov (raw)", "Filled", "Shortest and Filled"),) + 
  #scale_fill_brewer(palette="RdBu",name = "Trace", labels = c("GM", "MG", "PRW","RWP")) +
  scale_fill_grey(start = 1, end = 0.5) +
  theme_minimal()  +#+ theme(legend.position = "none") + 
  theme(legend.position="none",#axis.text.x = element_blank(),
        axis.text=element_text(size=10),
        axis.title=element_text(size=10),legend.title=element_text(size=10), 
        legend.text=element_text(size=10),strip.text.x = element_text(size = 10)) +
  labs(x="Traces")+
  facet_wrap(~Feature, scales = "free")  

plot(p)







