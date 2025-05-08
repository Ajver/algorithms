mgcd :: Int -> Int -> Int
mgcd a 0 = a
mgcd a b
  | a >= b    = mgcd (a - b) b
  | otherwise = mgcd (b - a) a
  
agcd :: Int -> Int -> Int
agcd a b = mgcd (abs a) (abs b)


sumOfDigits :: Int -> Int
sumOfDigits 0 = 0
sumOfDigits a
  | a < 0     = sumOfDigits (-a)
  | a < 10    = a
  | otherwise = (a `mod` 10) + sumOfDigits (a `div` 10)


collatzSequenceLength :: Int -> Int
collatzSequenceLength n = collatzSequenceLengthImpl n 0

collatzSequenceLengthImpl :: Int -> Int -> Int
collatzSequenceLengthImpl 1 i = i
collatzSequenceLengthImpl n i
  | n `mod` 2 == 0 = collatzSequenceLengthImpl (n `div` 2) (i + 1)
  | otherwise      = collatzSequenceLengthImpl ((3 * n) + 1) (i + 1)

main :: IO ()
main = do
    line <- getLine
    let a = read line :: Int
    
    line <- getLine
    let b = read line :: Int
    putStrLn $ show $ agcd a b
    putStrLn $ show $ sumOfDigits a
    putStrLn $ show $ sumOfDigits b
    if a > 0
      then putStrLn $ show $ collatzSequenceLength a
    else return ()
    
    if b > 0
      then putStrLn $ show $ collatzSequenceLength b
    else return ()