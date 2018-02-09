pdf("computation_times.pdf", width = 10, height = 5, pointsize = 12)
par(mfrow = c(1,2))

times_obssize <- read.csv(file = "computation_times_obssize_numba.csv", header = FALSE)
n <- as.numeric(times_obssize[3,])
time_psr <- as.numeric(times_obssize[1,])
time_st <- as.numeric(times_obssize[2,])

plotrange <- range(c(time_psr, time_st))
plot(n, time_psr, col = "orange", type = "o", ylim = plotrange,
     ylab = "computation time in seconds", xlab = "number of observations",
     main = "ensemble size fixed at 50")
lines(n, time_st, col = "purple", type = "o")
legend("topleft", lty = c(1,1), col = c("orange", "purple"), 
       legend = c("properscoring", "scoringtools"), bty = "n")

##

times_enssize <- read.csv(file = "computation_times_enssize_numba.csv", header = FALSE)
n <- as.numeric(times_enssize[3,])
time_psr <- as.numeric(times_enssize[1,])
time_st <- as.numeric(times_enssize[2,])

plotrange <- range(c(time_psr, time_st))
plot(n, time_psr, col = "orange", type = "o", ylim = plotrange,
     ylab = "computation time in seconds", xlab = "number of ensemble members",
     main = "number of observations fixed at 50")
lines(n, time_st, col = "purple", type = "o")
legend("topleft", lty = c(1,1), col = c("orange", "purple"), 
       legend = c("properscoring", "scoringtools"), bty = "n")

dev.off()