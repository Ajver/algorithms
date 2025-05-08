import Data.Char (ord)

listToStr :: [Int] -> String
listToStr [] = ""
listToStr [x] = show x
listToStr (x:xs) = (show x) ++ " " ++ (listToStr xs)


floatListToStr :: [Float] -> String
floatListToStr [] = ""
floatListToStr [x] = show x
floatListToStr (x:xs) = (show x) ++ " " ++ (floatListToStr xs)


main :: IO ()
main = do
  input <- getLine
  let n = read input :: Int
  putStrLn $ listToStr [n..(n+20)]
  putStrLn $ listToStr [(n+15), (n+14)..(n+2)]
  let nFloat = fromIntegral n :: Float
  putStrLn $ floatListToStr [nFloat, nFloat+0.125 .. nFloat+16.0]
  putStrLn $ show $ [c | c <- ['a'..'z'], ord c `mod` 2 /= 0]
