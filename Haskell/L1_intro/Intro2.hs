max3 :: Int -> Int -> Int -> Int
max3 a b c
    | a >= b && a >= c = a
    | b >= a && b >= c = b
    | otherwise = c
  

min3 :: Int -> Int -> Int -> Int
min3 a b c
    | a <= b && a <= c = a
    | b <= a && b <= c = b
    | otherwise = c


isPrime :: Int -> Bool
isPrime n = isPrimeImpl 2 n

isqrt :: Int -> Int
isqrt = floor . sqrt . fromIntegral

isPrimeImpl :: Int -> Int -> Bool
isPrimeImpl a b
    | a > isqrt b = True
    | b `mod` a == 0 = False
    | otherwise = isPrimeImpl (a+1) b

writeSymbols :: Char -> Int -> IO ()
writeSymbols _ 0 = return ()
writeSymbols c n = do
    if n > 0 then do
        putChar c
        writeSymbols c (n-1)
    else return ()

main :: IO ()
main = do
    input <- getLine
    let a = read input :: Int
    input <- getLine
    let b = read input :: Int
    input <- getLine
    let c = read input :: Int
    
    let minNum = (min3 a b c)
    let maxNum = (max3 a b c)

    print (minNum + maxNum)
    
    if isPrime a then print a
    else do
        if isPrime b then print b
        else do
            if isPrime c then print c
            else print "BRAK"
    
    writeSymbols 'x' minNum