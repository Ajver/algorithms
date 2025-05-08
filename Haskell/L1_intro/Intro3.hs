minmax2 :: Int -> Int -> (Int, Int)
minmax2 a b
  | a <= b    = (a, b)
  | otherwise = (b, a)


minmax4 :: Int -> Int -> Int -> Int -> (Int, Int)
minmax4 a b c d =
    let (a1min, a1max) = minmax2 a b
        (a2min, a2max) = minmax2 c d
    in (min a1min a2min, max a1max a2max)
 

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
    putChar c
    writeSymbols c (n-1)

main :: IO ()
main = do
    input <- getLine
    let a = read input :: Int
    input <- getLine
    let b = read input :: Int
    input <- getLine
    let c = read input :: Int
    input <- getLine
    let d = read input :: Int
    
    let (min4, max4) = minmax4 a b c d

    putStrLn $ show $ (min4 + max4)
    if isPrime a then
        putStrLn $ show a
    else do
        if isPrime b then print b
        else do
            if isPrime c then print c
            else do
                if isPrime d then print d
                else print "BRAK"
                
    writeSymbols 'x' min4

