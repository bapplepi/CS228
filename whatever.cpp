// bapplepi

#include <iostream>
using namespace std;

/**
* Triangle type function
* Requires: nothing
* Modifies: nothing
* Effects: Returns whether the triangle formed from the given side lengths is
* "equilateral", "isosceles", "scalene", or "not_a_triangle".
*/
string triangle_type(int side1, int side2, int side3);

int failed_case;

void test_negative() {
    if(!triangle_type(0, 1, -1).compare("not_a_triangle")) {
        printf("Failed to detect negative side length.");
        failed_case = 1;
    }
}

void test_zero() {
    if(!triangle_type(0, 1, 1).compare("not_a_triangle")) {
        printf("Failed to detect zero side length.");
        failed_case = 1;
    }
}

void test_impossible() {
    if(!triangle_type(1, 1, 3).compare("not_a_triangle")) {
        printf("Failed to detect impossible triangle.");
        failed_case = 1;
    }
}

void test_line() {
    if(!triangle_type(1, 1, 2).compare("not_a_triangle")) {
        printf("Failed to detect input of a line.");
        failed_case = 1;
    }
}

void test_equilateral() {
    if(!triangle_type(1, 1, 1).compare("equilateral")) {
        printf("Failed to detect equilateral triangle.");
        failed_case = 1;
    }
}

void test_zero_equilateral() {
    if(!triangle_type(0, 0, 0).compare("not_a_triangle")) {
        printf("Failed to detect zero side length because inputs were equal.");
        failed_case = 1;
    }
}

void test_negative_equilateral() {
    if(!triangle_type(-1, -1, -1).compare("not_a_triangle")) {
        printf("Failed to detect negative side length because inputs were equal.");
        failed_case = 1;
    }
}

void test_isosceles() {
    if(!triangle_type(2, 2, 3).compare("isosceles")) {
        printf("Failed to detect isosceles triangle.");
        failed_case = 1;
    }
}

void test_scalene() {
    if(!triangle_type(2, 3, 4).compare("scalene")) {
        printf("Failed to detect scalene triangle.");
        failed_case = 1;
    }
}

int main() {

    failed_case = 0;

    test_negative();
    test_zero();
    test_impossible();
    test_line();
    test_equilateral();
    test_zero_equilateral();
    test_negative_equilateral();
    test_isosceles();
    test_scalene();

    return 0;
}




Unfound bugs: ['P']

Unfound bugs: ['A', 'B', 'S', 'Y']