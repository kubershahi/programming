#include <iostream>
#include <string>
#include <algorithm>

class Manipulate {
public:
    Manipulate(const std::string& text) : text(text) {}

    std::string reverse() {
        int l = 0, r = text.size() - 1;
        while (l < r) {
            std::swap(text[l], text[r]);
            l++;
            r--;
        }
        return text;
    }

private:
    std::string text;
};

int main() {
    Manipulate string_manipulator("hello");
    std::string reversed_text = string_manipulator.reverse();
    std::cout << reversed_text << std::endl;
    return 0;
}