
add :: Float -> Float -> Float
add a b = a + b

sub :: Float -> Float -> Float
sub a b = a - b

mul :: Float -> Float -> Float
mul a b = a * b

divider :: Float -> Float -> Float
divider a b = a / b


getFunction 1 = add
getFunction 2 = sub
getFunction 3 = mul
getFunction 4 = divider


getFunctionSign :: Int -> String
getFunctionSign 1 = " + "
getFunctionSign 2 = " - "
getFunctionSign 3 = " * "
getFunctionSign 4 = " / "

isValidChoice :: Int -> Bool
isValidChoice choice = choice >= 1 && choice <= 4


main :: IO ()
main = do
  line <- getLine
  let a = read line :: Float
  line <- getLine
  let b = read line :: Float
  
  line <- getLine
  let choice = read line :: Int
  
  if not (isValidChoice choice) then do 
    putStrLn $ "Error! Unknown choice: " ++ show choice
    return ()
  else do
    putStr $ show a ++ (getFunctionSign choice) ++ show b ++ " = "
    putStrLn $ show $ (getFunction choice) a b
