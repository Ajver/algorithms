#include <iostream>
#include <stdexcept>

using namespace std;


int NWD(int a, int b)
{
   if(a!=b)
     return NWD(a>b?a-b:a,b>a?b-a:b);

   return a;
}

class LiczbaWym {
    public:
        int licznik;
        int mianownik;
        
        LiczbaWym(int l, int m) {
            if (m == 0) {
                throw overflow_error("Divide by zero exception");
            }

            int nwd = NWD(abs(l), abs(m));
            if (nwd > 1) {
                l /= nwd;
                m /= nwd;
            }

            licznik = l;
            mianownik = m;
        }

        LiczbaWym odwrotnosc() const {
            return LiczbaWym(mianownik, licznik);
        }

        LiczbaWym operator +(const LiczbaWym &b) const {
            int nl = licznik * b.mianownik + mianownik * b.licznik;
            int nm = mianownik * b.mianownik;
            return LiczbaWym(nl, nm);
        }

        LiczbaWym operator -(const LiczbaWym &b) const {
            int nl = licznik * b.mianownik - mianownik * b.licznik;
            int nm = mianownik * b.mianownik;
            return LiczbaWym(nl, nm);
        }

        LiczbaWym operator *(const LiczbaWym &b) const {
            int nl = licznik * b.licznik;
            int nm = mianownik * b.mianownik;
            return LiczbaWym(nl, nm);
        }

        LiczbaWym operator /(const LiczbaWym &b) const {
            LiczbaWym bodw = b.odwrotnosc();
            return (*this) * (b.odwrotnosc());
            // return (*this) * bodw;
        }

        void wyswietl() {
            cout << licznik << "/" << mianownik << " ";
        }

};


int main() {
    int la = 2;
    int ma = 3;
    int lb = 3;
    int mb = 4;
    char oper = '/';

    // cout << "Podaj licznik a: ";
    // cin >> la;

    // cout << "Podaj mianownik a: ";
    // cin >> ma;

    // cout << "Podaj operację: (+-*/): ";
    // cin >> oper;

    // cout << "Podaj licznik b: ";
    // cin >> lb;
    // cout << "Podaj mianownik b: ";
    // cin >> mb;

    try {
        LiczbaWym a(la, ma);
        LiczbaWym b(lb, mb);

        a.wyswietl();
        cout << oper << " ";
        b.wyswietl();
        cout << " = ";

        LiczbaWym c(1, 1);

        switch(oper) {
            case '+': c = a + b; break;
            case '-': c = a - b; break;
            case '*': c = a * b; break;
            case '/': c = a / b; break;
            default:
                cout << "Nieznana operacja: " << oper << endl;
                return 2;
        }

        c.wyswietl();

    }catch (overflow_error &e) {
        cout << "Error: " << e.what() << endl;
        return 2;
    }
    
    return 0;
}