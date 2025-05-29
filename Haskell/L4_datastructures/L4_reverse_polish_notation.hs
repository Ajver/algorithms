import Control.Monad (foldM)

----------------------------------------------------------------
-- Algebraiczny typ danych dla kalkulatora odwrotnej notacji Polskiej (ONP)
----------------------------------------------------------------

-- | Algebraiczny typ danych reprezentujący wyrażenia
data Expr
    = Const Integer      -- stała
    | Add Expr Expr      -- suma
    | Sub Expr Expr      -- różnica
    | Mul Expr Expr      -- mnożenie
    | Div Expr Expr      -- dzielenie
    deriving (Show, Eq)

-- Funkcja do ewaluacji wyrażenia
eval :: Expr -> Integer
eval (Const x) = x
eval (Add x y) = eval x + eval y
eval (Sub x y) = eval x - eval y
eval (Mul x y) = eval x * eval y
eval (Div x y) = (eval x) `div` (eval y)

-- pomocnicza funkcja do wielokrotnego stosowania funkcji na liście z propagacją błędów
foldEither :: (a -> b -> Either String a) -> a -> [b] -> Either String a
foldEither _ acc []     = Right acc
foldEither f acc (x:xs) =
    case f acc x of
      Left err   -> Left err
      Right acc' -> foldEither f acc' xs

-- sparsuj wyrażenie podane jako ciąg znaków do algebraicznego typu danych Expr
parseRPN :: String -> Either String Expr
parseRPN input =
  let exprStack = foldEither step [] (words input)
  in case exprStack of
    Left str -> Left str
    Right [expr] -> Right expr
    Right _ -> Left "na stosie pozostały niewykorzystane elementy"
  where
    step :: [Expr] -> String -> Either String [Expr]
    step stack token =
      case token of
        "+" -> applyOp token Add stack
        "-" -> applyOp token Sub stack
        "*" -> applyOp token Mul stack
        "/" -> applyOp token Div stack
        otherwise   -> Right $ Const (read token :: Integer) : stack
            
    -- Zastosuj podany operator do stosu
    -- odłóż wynik na stos
    applyOp :: String -> (Expr -> Expr -> Expr) -> [Expr] -> Either String [Expr]
    applyOp _ op (x:y:rest) = Right ((y `op` x) : rest)
    applyOp token _ _ = Left $ "za mało argumentów dla operatora " ++ token

-- Oblicz wartość wyrażenia ONP podanego jako String
evalRPN :: String -> Either String Integer
evalRPN s =
  case parseRPN s of
    Left str -> Left str
    Right expr -> Right $ eval expr

-- funkcja main
main :: IO ()
main = do
  input <- getLine
  case evalRPN input of
    Left err -> putStrLn ("Błąd: " ++ err)
    Right result -> putStrLn $ "Wynik: " ++ show result
