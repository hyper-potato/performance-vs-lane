library(dplyr)
library(ggplot2)
library(MatchIt)

df = read.csv('clean_2.csv')
df$Improvement = df$SeedTime - df$PrelimsTime

hist(df$PrelimsTime)
hist(df$FinalsTime)
hist(df$Improvement, breaks = 20)

ggplot(df, aes(x = Gender)) + geom_bar()
ggplot(df, aes(x = Stroke)) + geom_bar()
ggplot(df, aes(x = Lane)) + geom_bar()

ggplot(df, aes(x = PrelimsTime, y = FinalsTime)) + geom_point()
ggplot(df, aes(x = PrelimsTime, y = Improvement)) + geom_point()
ggplot(df, aes(x = FinalsTime, y = Improvement)) + geom_point()
cor(df$PrelimsTime, df$FinalsTime)
cor(df$PrelimsTime, df$Improvement)
cor(df$FinalsTime, df$Improvement)

model_naivea = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = df)
model_naiveb = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane + Gender:Stroke, data = df)
summary(model_naivea)
summary(model_naiveb)

ggplot(df, aes(x = PrelimsTime, fill = Lane)) + geom_density(alpha = 0.5)
ggplot(df, aes(x = FinalsTime, fill = Lane)) + geom_density(alpha = 0.5)

ggplot(df, aes(x = FinalsTime, fill = Gender)) + geom_density(alpha = 0.5)
ggplot(df, aes(x = FinalsTime, fill = Stroke)) + geom_density(alpha = 0.5)
ggplot(df, aes(x = FinalsTime, fill = Gender)) + geom_density(alpha = 0.5) + facet_wrap(~ Stroke)

mean(df[df$Lane == 'Outside',]$PrelimsTime)
mean(df[df$Lane == 'Inside',]$PrelimsTime)
mean(df[df$Lane == 'Outside',]$FinalsTime)
mean(df[df$Lane == 'Inside',]$FinalsTime)

t.test(PrelimsTime ~ Lane, data = df)
t.test(Improvement ~ Lane, data = df)

n_outside = summary(df$Lane)[2]
n_inside = summary(df$Lane)[1]
summary(df[df$Lane == 'Outside',]$Gender) / n_outside
summary(df[df$Lane == 'Inside',]$Gender) / n_inside
summary(df[df$Lane == 'Outside',]$Stroke) / n_outside
summary(df[df$Lane == 'Inside',]$Stroke) / n_inside

ps_model = glm(Lane ~ PrelimsTime, data = df, family = 'binomial')
df$PS = ps_model$fitted.values
ggplot(df, aes(x = PS, fill = Lane)) + geom_density(alpha = 0.5)

df$Lane = ifelse(df$Lane == 'Outside', 1, 0)
match_output = matchit(Lane ~ PrelimsTime, data = df, method = 'nearest', distance = 'logit', caliper = 0.05, replace = FALSE, ratio = 1)
summary(match_output)
df_match = match.data(match_output)

t.test(PrelimsTime ~ Lane, data = df_match)
ggplot(df_match, aes(x = PS, fill = factor(Lane))) + geom_density(alpha = 0.5)
t.test(Improvement ~ Lane, data = df_match)

n_outside_match = summary(factor(df_match$Lane))[1]
n_inside_match = summary(factor(df_match$Lane))[2]
summary(df_match[df_match$Lane == 1,]$Gender) / n_outside_match
summary(df_match[df_match$Lane == 0,]$Gender) / n_inside_match
summary(df_match[df_match$Lane == 1,]$Stroke) / n_outside_match
summary(df_match[df_match$Lane == 0,]$Stroke) / n_inside_match

model_matcha = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane, data = df_match)
model_matchb = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Improvement + Lane + Gender:Stroke, data = df_match)
summary(model_matcha)
summary(model_matchb)

ps_model2 = glm(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, family = 'binomial')
df$PS2 = ps_model2$fitted.values
ggplot(df, aes(x = PS2, fill = factor(Lane))) + geom_density(alpha = 0.5)

match_output2 = matchit(Lane ~ PrelimsTime + Gender + Stroke + Improvement, data = df, method = 'nearest', distance = 'logit', caliper = 0.01, replace = FALSE, ratio = 1)
summary(match_output2)
df_match2 = match.data(match_output2)

t.test(PrelimsTime ~ Lane, data = df_match2)
t.test(Improvement ~ Lane, data = df_match2)

n_outside_match2 = summary(factor(df_match2$Lane))[1]
n_inside_match2 = summary(factor(df_match2$Lane))[2]
summary(df_match2[df_match2$Lane == 1,]$Gender) / n_outside_match2
summary(df_match2[df_match2$Lane == 0,]$Gender) / n_inside_match2
summary(df_match2[df_match2$Lane == 1,]$Stroke) / n_outside_match2
summary(df_match2[df_match2$Lane == 0,]$Stroke) / n_inside_match2
ggplot(df_match2, aes(x = PS2, fill = factor(Lane))) + geom_density(alpha = 0.5)

model_match2a = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Lane + Improvement, data = df_match2)
model_match2b = lm(FinalsTime ~ PrelimsTime + Gender + Stroke + Lane + Improvement + Gender:Stroke, data = df_match2)
summary(model_match2a)
summary(model_match2b)
