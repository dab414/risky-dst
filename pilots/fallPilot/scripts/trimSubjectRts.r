trimSubjectRts <- function(d){
  ## takes in data and trims based on +/- 2 SDs off subject-wise means
  
  d <- d %>% 
    group_by(subject) %>% 
    summarize(meanRt = mean(rt), sdRt = sd(rt)) %>% 
    inner_join(d) %>% 
    filter(rt > meanRt - 2 * sdRt & rt < meanRt + 2 * sdRt) %>% 
    select(-meanRt, -sdRt)
  
  
  return(d)
  
  
}