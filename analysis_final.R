library(dplyr)
library(ggplot2)
library(MatchIt)
library(ggthemes)

df = read.csv('clean_2.csv')

# Define improvement as difference from seed time to prelims time 
df$Improvement = df$SeedTime - df$PrelimsTime

# Keep name of lane (i.e. inside or outside) for graphing purposes 
df$LaneName = df$Lane
df$Lane = ifelse(df$Lane == 'Outside', 1, 0)

### Data Exploration ###
## Figure 1 ##
ggplot(df, aes(x = PrelimsTime)) + 
  theme_economist() + 
  geom_histogram() + 
  labs(x = 'Prelims Time', y = 'Count', title = 'Distribution of Prelims Time') + 
  scale_fill_economist()

ggplot(df, aes(x = FinalsTime)) + theme_economist() + geom_histogram() + 
  labs(x = 'Finals Time', y = 'Count', title = 'Distribution of Finals Time') + 
  scale_fill_economist()
ggplot(df, aes(x = Improvement)) + 
  theme_economist() + geom_histogram() + 
  geom_vline(xintercept = 0, color = 'white', linetype = 'dashed') + 
  labs(x = 'Improvement', y = 'Count', title = 'Distribution of Improvement') + 
  scale_fill_economist()

## Figure 2 ##
ggplot(df, aes(x = Gender, fill = Gender)) + theme_economist() + geom_bar() + theme(legend.position = 'none') + labs(y = 'Count', title = 'Distribution of Gender') + scale_fill_economist()
ggplot(df, aes(x = Stroke, fill = Stroke)) + theme_economist() + geom_bar() + theme(legend.position = 'none') + labs(y = 'Count', title = 'Distribution of Stroke') + scale_fill_economist()
ggplot(df, aes(x = LaneName, fill = LaneName)) + theme_economist() + geom_bar() + theme(legend.position = 'none') + labs(y = 'Count', title = 'Distribution of Treatment') + scale_fill_economist()


## Figure 3 ##
ggplot(df, aes(x = PrelimsTime, y = FinalsTime)) + theme_economist() + scale_fill_economist() + geom_point() + labs(x = 'Prelims Time', y = 'Finals Time', title = 'Correlation of .994 between \nPrelims and Finals Time')
ggplot(df, aes(x = FinalsTime, fill = Gender)) + theme_economist() + scale_fill_economist() + geom_density(alpha = 0.5) + labs(x = 'Finals Time', y = 'Density', title = 'Finals Performance by Gender')
ggplot(df, aes(x = FinalsTime, fill = Stroke)) + theme_economist() + scale_fill_economist() + geom_density(alpha = 0.5) + labs(x = 'Finals Time', y = 'Density', title = 'Finals Performance by Stroke')

cor(df$PrelimsTime, df$FinalsTime)


### Main Analysis ###
# Run a regression without any matching
model_naive = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = df) 
summary(model_naive)
# t-tests show that both prelims time and improvement vary greatly between treatment groups 
t.test(PrelimsTime ~ Lane, data = df)
t.test(Improvement ~ Lane, data = df)

# Gender is very balanced between groups
summary(df[df$Lane == 1,]$Gender) / summary(factor(df$Lane))[2] 
summary(df[df$Lane == 0,]$Gender) / summary(factor(df$Lane))[1]

# Strokes are also quite balanced across treatment groups 
summary(df[df$Lane == 1,]$Stroke) / summary(factor(df$Lane))[2] 
summary(df[df$Lane == 0,]$Stroke) / summary(factor(df$Lane))[1]
# Preparing dataframes for plotting Figure 4 
prelims_outside = mean(df[df$Lane == 1,]$PrelimsTime) 
prelims_inside = mean(df[df$Lane == 0,]$PrelimsTime) 
improve_outside = mean(df[df$Lane == 1,]$Improvement) 
improve_inside = mean(df[df$Lane == 0,]$Improvement)

graph = data.frame(PrelimsTime = c(prelims_outside, prelims_inside)) 
graph2 = data.frame(Improvement = c(improve_outside, improve_inside)) 
graph$Lane = c('Outside', 'Inside')
graph2$Lane = c('Outside', 'Inside')

# Fit propensity score model
ps_model = glm(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, family = 'binomial')
df$PS = ps_model$fitted.values

## Figure 4 ##
ggplot(graph, aes(x = Lane, y = PrelimsTime, fill = Lane)) + 
  theme_economist() + scale_fill_economist() + 
  geom_col() + geom_text(aes(label = round(PrelimsTime, 2)), stat = "identity", vjust = -.15) + 
  theme(legend.position = 'none') + labs(y = 'Prelims Time', title = 'Unbalanced Speed Across Groups')

ggplot(graph2, aes(x = Lane, y = Improvement, fill = Lane)) + theme_economist() + scale_fill_economist() + 
  geom_col() + geom_text(aes(label = round(Improvement, 2)), stat = "identity", vjust = -.15) + theme(legend.position = 'none') + 
  labs(title = 'Unbalanced Improvement \nAcross Groups')

ggplot(df, aes(x = PS, fill = LaneName)) + theme_economist() + scale_fill_economist() + 
  geom_density(alpha = 0.5) + labs(x = 'Propensity Score', y = 'Density', title = 'Misalignment Before Matching')

# Match based on propensity scores
match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, 
                       method = 'nearest', distance = 'logit', caliper = 0.01, replace = FALSE, ratio = 1) 
summary(match_output)
df_match = match.data(match_output)

# t-tests show insignificant differences in prelims time and improvement across treatment groups 
t.test(PrelimsTime ~ Lane, data = df_match)
t.test(Improvement ~ Lane, data = df_match)

# Gender seems balanced across treatment groups
summary(df_match[df_match$Lane == 1,]$Gender) / summary(factor(df_match$Lane))[2] 
summary(df_match[df_match$Lane == 0,]$Gender) / summary(factor(df_match$Lane))[1]

# Strokes also appear fairly balanced between groups, although there is slight imbalance in backstroke and freestyle
summary(df_match[df_match$Lane == 1,]$Stroke) / summary(factor(df_match$Lane))[2] 
summary(df_match[df_match$Lane == 0,]$Stroke) / summary(factor(df_match$Lane))[1]

# Preparing dataframes for plotting Figure 5
match_prelims_outside = mean(df_match[df_match$Lane == 1,]$PrelimsTime) 
match_prelims_inside = mean(df_match[df_match$Lane == 0,]$PrelimsTime) 
match_improve_outside = mean(df_match[df_match$Lane == 1,]$Improvement) 
match_improve_inside = mean(df_match[df_match$Lane == 0,]$Improvement)
match_graph = data.frame(PrelimsTime = c(match_prelims_outside, match_prelims_inside)) 
match_graph2 = data.frame(Improvement = c(match_improve_outside, match_improve_inside)) 
match_graph$Lane = c('Outside', 'Inside')
match_graph2$Lane = c('Outside', 'Inside')

## Figure 5 ##
ggplot(match_graph, aes(x = Lane, y = PrelimsTime, fill = Lane)) + theme_economist() + scale_fill_economist() + 
  geom_col() + geom_text(aes(label = round(PrelimsTime, 2)), stat = "identity", vjust = -.15) + theme(legend.position = 'none') + 
  labs(y = 'Prelims Time', title = 'Balanced Speed After Matching')
ggplot(match_graph2, aes(x = Lane, y = Improvement, fill = Lane)) + theme_economist() + scale_fill_economist() + 
  geom_col() + geom_text(aes(label = round(Improvement, 2)), stat = "identity", vjust = -.15) + theme(legend.position = 'none') + labs(title = 'Balanced Improvement \nAfter Matching')
ggplot(df_match, aes(x = PS, fill = LaneName)) + theme_economist() + scale_fill_economist() + 
  geom_density(alpha = 0.5) + labs(x = 'Propensity Score', y = 'Density', title = 'Alignment After Matching')

# Re-run regression on matched dataframe
model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = df_match)
summary(model_match)

### Sensitivity Analysis ###
# Different caliper values
c1_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, method = 'nearest', distance = 'logit', caliper = 0.005, replace = FALSE, ratio = 1) 
summary(c1_match_output)
c1_df_match = match.data(c1_match_output)
c1_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = c1_df_match)
summary(c1_model_match)

c2_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, method = 'nearest', distance = 'logit', caliper = 0.1, replace = FALSE, ratio = 1) 
summary(c2_match_output)
c2_df_match = match.data(c2_match_output)
c2_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = c2_df_match)
summary(c2_model_match)

# Different functional form
p_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, 
                         method = 'nearest', distance = 'probit', caliper = 0.01, replace = FALSE, ratio = 1) 
summary(p_match_output)
p_df_match = match.data(p_match_output)

p_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = p_df_match)
summary(p_model_match)

# Different ratio of control and treatment
r_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, method = 'nearest', distance = 'logit', caliper = 0.01, replace = FALSE, ratio = 2) 
summary(r_match_output)
r_df_match = match.data(r_match_output)
r_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = r_df_match)
summary(r_model_match)


# Sampling with replacement
wr_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, method = 'nearest', distance = 'logit', caliper = 0.01, replace = TRUE, ratio = 1) 
summary(wr_match_output)
wr_df_match = match.data(wr_match_output)
wr_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = wr_df_match)
summary(wr_model_match)

# Different matching methods
m1_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, 
                          method = 'genetic', distance = 'logit', caliper = 0.2, replace = FALSE, ratio = 1) 
# Higher caliper necessary to find sufficient matches
summary(m1_match_output)
m1_df_match = match.data(m1_match_output)

m1_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = m1_df_match)
summary(m1_model_match)
m2_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, 
                          method = 'optimal', distance = 'logit', caliper = 0.01, replace = FALSE, ratio = 1) 
summary(m2_match_output)
m2_df_match = match.data(m2_match_output)
m2_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = m2_df_match)
summary(m2_model_match)

# Matching on subsets of variables
s1_match_output = matchit(Lane ~ PrelimsTime, data = df, method = 'nearest', distance = 'logit', caliper = 0.01, replace = FALSE, ratio = 1)
summary(s1_match_output)
s1_df_match = match.data(s1_match_output)
s1_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = s1_df_match)
summary(s1_model_match)
s2_match_output = matchit(Lane ~ PrelimsTime + Gender + Stroke, data = df, method = 'nearest', distance = 'logit', caliper = 0.01, replace = FALSE, ratio = 1)
summary(s2_match_output)
s2_df_match = match.data(s2_match_output)
s2_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = s2_df_match)
summary(s2_model_match)

# Regression with interactions
i1_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane + Gender:Stroke, data = df_match)
summary(i1_model_match)

i2_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane + Gender:Lane, data = df_match)
summary(i2_model_match)

i3_model_match = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane + Stroke:Lane, data = df_match)
summary(i3_model_match)

