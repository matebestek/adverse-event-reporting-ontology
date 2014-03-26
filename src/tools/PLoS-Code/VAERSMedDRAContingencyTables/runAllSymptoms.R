# First, read the CSV document in as a matrix.
# The option 'header=F' tells it not to treat the first row as a header/column names.
# The option stringsAsFactors=F tells it to treat words as individual words, not as factors (e.g. it would transform "Male" "Female" into numeric variables if it suspects it's a repeated variable. This might be the case but it gets confusing fast!)
M <- read.csv('./ListMedDRATermsAndOutcome.csv', header=F, stringsAsFactors=F)

# Give informative column names to the data matrix:
colnames(M) <- c("Diagnosis", "Report ID", "Symptom1", "Symptom2", "Symptom3", "Symptom4", "Symptom5")

# To cycle through all the reports, first identify the unique report IDs and cycle through those instead of through rows of the data matrix.
unique.ids <- unique(M[, "Report ID"])

# We will also cycle through each unique symptom. First, concatenate the 3rd to the 7th column of the data matrix (where the symptoms are stored), then identify the unique ones:
symptom.list <- unique(as.character(unlist(M[, 3:7])))

# Initialize a matrix to store results. The row names will be the symptoms, and each row will have three entries: the Chi-squared statistic (the value you want to be high), the p-value associated with the chi-squared test, and the Odds ratio. The first two tell you about the significance of that symptom, while the odds ratio tells you which direction it is significant in -- if it is greater than 1, then the symptom is more common in people WITH anaphylaxis. If it is less than 1 -- then it is more common in people WITHOUT anaphylaxis.

results <- matrix(0, nrow = length(symptom.list), ncol = 3)
colnames(results) <- c("Chi-square", "P-value", "Odds Ratio (Anaphylaxis/Not)")
rownames(results) <- symptom.list

for (symptom in symptom.list){
  # Define 4 numbers:
  # a = # patients with positive diagnosis and symptom present
  # b = # patients with positive diagnosis and lacking symptom
  # c = # patients with negative diagnosis and symptom present
  # d = # patients with negative diagnosis and lacking symptom

  # Initialize to 0.
  a <- b <- c <- d <- 0
  for(i in unique.ids){
    indices <- which(M[, "Report ID"] == i)
    all.symptoms <- as.character(unlist(M[indices, 3:7]))
    symptom.present <- any(grepl(symptom, all.symptoms, ignore.case=TRUE))
    pos.diagnosis <- grepl('positive', M[indices[1], "Diagnosis"], ignore.case=TRUE)
    
    if (pos.diagnosis && symptom.present){
      a <- a + 1
    } else if (pos.diagnosis && !symptom.present){
      b <- b + 1
    } else if (!pos.diagnosis && symptom.present){
      c <- c + 1
    } else if (!pos.diagnosis && !symptom.present){
      d <- d + 1
    }
  }

  # Now using those four numbers, build the contingency table:
  T <- rbind(c(a, b), c(c, d))
  rownames(T) <- c("Positive Diagnosis", "Negative Diagnosis")
  colnames(T) <- c("Symptom Present", "Symptom Absent")

  # Chi-squared test on this table tells us whether this symptom occurs in pattern with the diagnosis (anaphylaxis) or not:
  X <- chisq.test(T)
  # a/b is the ratio of anaphylactic patients with that symptom vs anaphylactic patients lacking that symptom. You want this to be high.
  # c/d is the ratio of "healthy" patients with that symptom vs "healthy" patients without that symptom. You want this to be low.
  # Now taking the ratios of the above ratios, if the value is > 1 then the presence of the symptom favours anaphylaxis.
  # If the value is < 1 then the presence of the symptom favours healthy status.
  # Note that this does not mean if you have this symptom, you are likely to have anaphylaxis. It just means you are
  odds.ratio <- (a/b)/(c/d) 
  results[symptom, "Chi-square"] <- X$statistic
  results[symptom, "P-value"] <- X$p.value
  results[symptom, "Odds Ratio (Anaphylaxis/Not)"] <- odds.ratio
}

# Use the Chi-square statistic column to sort the report.
sort.indices <- sort(results[, "Chi-square"], decreasing = TRUE, index.return=TRUE)$ix 
sort.results <- results[sort.indices, ]
# Write the result to a csv file:
write.csv(sort.results, file = "symptomSignificance.csv")

