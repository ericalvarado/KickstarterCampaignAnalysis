library(readxl)
outputfile_070015_v2 <- read_excel("Dropbox/CUS615 - Data Mining 2/Project/JSON Data/outputfile_070015_v3.xlsx", col_types = c("blank", "text", "blank","text", "text", "numeric", "numeric","numeric", "blank", "numeric", "numeric","text", "numeric", "text", "numeric","numeric", "numeric", "numeric","numeric", "numeric", "numeric","date", "date", "date"))
View(outputfile_070015_v2)

ksData <- outputfile_070015_v2
dim(ksData)
names(ksData)

options(max.print = 100000)

ksDF <- data.frame(ksData)
keepVariables <- c("name","country","goal","backerCount","pledgedAmount","url","spotlight","staffPick","imgCount","embedCount","pCount","wordCount","pctOUGoal","LaunchedAtDate","DeadlineDate","StateChangeDate")
kickstartDF<-ksDF[keepVariables]
kickstartDF["backerPledgeAmountRatio"]<-kickstartDF$pledgedAmount/kickstartDF$backerCount

dim(kickstartDF)
names(kickstartDF)

library(ggplot2)
# Reference: http://www.sthda.com/english/wiki/ggplot2-scatter-plots-quick-start-guide-r-software-and-data-visualization

# Histograms of the independent variables
ggplot(kickstartDF, aes(x=imgCount),stat="count") + geom_histogram() +labs(title="Figure 1: Histogram of Image Count",x="Number of Images", y = "Frequency") + theme_classic()
ggplot(kickstartDF, aes(x=embedCount),stat="count") + geom_histogram() +labs(title="Figure 2: Histogram of Embed Count",x="Number of Embeds", y = "Frequency") + theme_classic()
ggplot(kickstartDF, aes(x=pCount),stat="count") + geom_histogram() +labs(title="Figure 3: Histogram of Paragraph Count",x="Number of Paragraphs", y = "Frequency") + theme_classic()
ggplot(kickstartDF, aes(x=wordCount),stat="count") + geom_histogram() +labs(title="Figure 4: Histogram of Word Count",x="Number of Words", y = "Frequency") + theme_classic()

# Scatterplot of the independent variables over the dependent variable (pctOUGoal)
ggplot(kickstartDF, aes(x=imgCount, y=backerCount)) + geom_point() +labs(title="Figure 5: Scatterplot of Image Count v Backer Count",x="Number of Images", y = "Number of Backers") + theme_classic()
ggplot(kickstartDF, aes(x=embedCount, y=backerCount)) + geom_point() +labs(title="Figure 6: Scatterplot of Embed Count v Backer Count",x="Number of Images", y = "Number of Backers") + theme_classic()
ggplot(kickstartDF, aes(x=pCount, y=pctOUGoal)) + geom_point()+labs(title="Figure 7: Scatterplot of Paragraph Count v Backer Count",x="Number of Images", y = "Number of Backers") + theme_classic()
ggplot(kickstartDF, aes(x=wordCount, y=pctOUGoal)) + geom_point()+labs(title="Figure 8: Scatterplot of Word Count v Backer Count",x="Number of Images", y = "Number of Backers") + theme_classic()

# Descriptive Statistics of independent variables
# Reference: http://www.sthda.com/english/wiki/descriptive-statistics-and-graphics
# Reference: http://www.sthda.com/english/wiki/ggpubr-create-easily-publication-ready-plots#at_pco=smlwn-1.0&at_si=5cab262466586242&at_ab=per-2&at_pos=0&at_tot=1

install.packages("pastecs")
library(pastecs)
res <- stat.desc(kickstartDF[c("backerCount","embedCount","pCount","wordCount","pctOUGoal")])
round(res, 2)

# Correlation
# Reference: http://www.sthda.com/english/wiki/correlation-matrix-a-quick-start-guide-to-analyze-format-and-visualize-a-correlation-matrix-using-r-software
round(cor(kickstartDF[c("backerCount","embedCount","pCount","wordCount","pctOUGoal")],use = "na.or.complete"),2)

# Linear Regression
fit<-lm(backerCount~imgCount+embedCount,data=kickstartDF,na.action=na.omit)
fit  # display a short summary of fit
summary(fit)  # display a comprehensive summary of fit

names(fit)    # display names of object inside fit
fit$coefficients  # display coefficients in fit
fit$fitted.values  # display vector of predicted values
fit$residuals     # display vector of residuals

# GAM
install.packages("gam") #General Additive Model
library("gam")
fitGAM <- gam(backerPledgeAmountRatio~s(imgCount)+s(embedCount),data=kickstartDF,na.action=na.omit) #Modelled as a smooth function
summary(fitGAM)
