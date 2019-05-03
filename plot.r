library (tidyverse)
library(readxl)

data = readxl::read_xlsx("rfriendly.xlsx")
View(data)

#data %>%
 # mutate(Algorithm = `Improved (O(N^2))`) %>%
  #ggplot(mapping = aes(x = `Test No`, y = Naieve, color = Algorithm)) + 
  #geom_line() + 
  #labs(title = "Improved vs Naive", x = "Test Number", y = "Time Taken in Seconds")
data %>%
  mutate(Naieve = Naieve * 1000000) %>%
  mutate(Algorithm = `Improved (O(N^2))`) %>%
  ggplot(mapping = aes(x = `Test No`, y = Naieve, color = Algorithm)) + 
  geom_line() + 
  labs(title = "Improved vs Optimal", x = "Test Number", y = "Time Taken in Micro Seconds")
