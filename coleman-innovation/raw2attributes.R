library(data.table)

attr.file <- 'raw/attributes.dat'

# scan column names
cols <- scan(attr.file, 'character',
             skip=4, n=13)

cols <- sapply(cols, function(x) chartr(' ', '_', x))

dat <- fread(attr.file, skip=18, col.names=cols)

# see codebook in readme
dat[, adoption_date := as.numeric(adoption_date)]
dat[adoption_date == 18, adoption_date := Inf]
dat[adoption_date == 98, adoption_date := NA]
dat[adoption_date == 99, adoption_date := NA]

na.9 <- tail(cols, -2)
dat[, (na.9) := lapply(na.9, function(x) ifelse(get(x) == 9, NA, get(x)))]

fwrite(dat, 'processed/attributes.csv')
