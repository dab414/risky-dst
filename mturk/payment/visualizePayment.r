library(tidyverse)

computeCost <- function(payment) {
	return(payment * 130 + (payment * 130 * 0.2))
}


d <- data.frame(payment = seq(1.5, 3, 0.1))
d$totalCost <- computeCost(d$payment)

m1 <- lm(totalCost ~ payment, data = d)
intercept <- m1$coefficients[1]
slope <- m1$coefficients[2]

d1 <- data.frame(targetPayment = 381 / slope, targetCost = 381)

ggplot(d, aes(x = payment, y = totalCost)) +
	geom_line(size = 2) +
	labs(
		title = 'Relationship Between Total Cost and Possible Payments',
		x = 'Payment Per Subject in Dollars',
		y = 'Total Cost in Dollars',
		caption = 'Dashed line represents the amount of $700 that is remaining') +
	geom_hline(yintercept = 381, linetype = 'dashed') +
	geom_point(data = d1, aes(x = targetPayment, y = targetCost), size = 3, color = 'red') +
	#annotate('text', data = d1, aes(x = targetPayment + 10, y = targetCost + 10), label = paste('(', round(d1$targetPayment[1], 2), ', ', d1$targetCost[1], ')', sep = '')) +
	geom_text(data = d1, aes(x = targetPayment, y = targetCost, label = paste('(', round(d1$targetPayment[1], 2), ', ', d1$targetCost[1], ')', sep = '')), hjust = -.5, vjust = 2) +
	theme_bw() 

ggsave('exp3Payments.png', width = 5.5, height = 3.5, units = 'in', dpi = 96)
