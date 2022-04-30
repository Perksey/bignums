import os

with open(os.path.join(os.path.dirname(__file__), "tests.rs"), "w") as f:
    f.write("use super::*;\n")
    f.write("\n")
    f.write("#[test]\n")
    f.write("fn test_mul64to128() {\n")
    for left in range(0, 18446744073709551616, int(18446744073709551616 / 7)):
        for right in range(0, 18446744073709551616, int(18446744073709551616 / 7)):
            expected = left * right
            expected_high = expected >> 64
            expected_low = expected & 0xFFFFFFFFFFFFFFFF
            f.write("    assert_eq!(\n")
            f.write(f"        mul64to128({left}_u64, {right}_u64),\n")
            f.write("        U128 {\n")
            f.write(f"            high: {expected_high}_u64,\n")
            f.write(f"            low: {expected_low}_u64\n")
            f.write("        }\n")
            f.write("    );\n")
    f.write("}\n")
    f.write("\n")
    f.write("#[test]\n")
    f.write("fn test_mul128() {\n")
    test_cases = {
        0x77777777777777777777777777777777: range(15),
        0x11111111111111111111111111111111: range(15),
        0x000000000000000000000000000000F0: (0x01000000000000000000000000000000,),
    }
    for left in test_cases:
        for right in test_cases[left]:
            left_high = left >> 64
            left_low = left & 0xFFFFFFFFFFFFFFFF
            right_high = right >> 64
            right_low = right & 0xFFFFFFFFFFFFFFFF
            expected = left * right
            expected_high = expected >> 64
            if expected_high & 0xFFFFFFFFFFFFFFFF != expected_high:
                break
            expected_low = expected & 0xFFFFFFFFFFFFFFFF
            f.write("    assert_eq!(\n")
            f.write("        mul128(\n")
            f.write("            U128 {\n")
            f.write(f"                high: {left_high}_u64,\n")
            f.write(f"                low: {left_low}_u64,\n")
            f.write("            },\n")
            f.write("            U128 {\n")
            f.write(f"                high: {right_high}_u64,\n")
            f.write(f"                low: {right_low}_u64,\n")
            f.write("            }\n")
            f.write("        ),\n")
            f.write("        U128 {\n")
            f.write(f"            high: {expected_high}_u64,\n")
            f.write(f"            low: {expected_low}_u64\n")
            f.write("        }\n")
            f.write("    );\n")
    f.write("}\n")
    f.write("\n")
    f.write("#[test]\n")
    f.write("fn test_mul128to256() {\n")
    for left in range(0, 0x77777777777777777777777777777777, 0x22222222222222222222222222222222):
        for right in range(0, 0x77777777777777777777777777777777, 0x11111111111111111111111111111111):
            left_high = left >> 64
            left_low = left & 0xFFFFFFFFFFFFFFFF
            right_high = right >> 64
            right_low = right & 0xFFFFFFFFFFFFFFFF
            expected = left * right
            expected_high = expected >> 128
            if expected_high & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF != expected_high:
                break
            expected_low = expected & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            expected_high_high = expected_high >> 64
            expected_high_low = expected_high & 0xFFFFFFFFFFFFFFFF
            expected_low_high = expected_low >> 64
            expected_low_low = expected_low & 0xFFFFFFFFFFFFFFFF
            f.write("    assert_eq!(\n")
            f.write("        mul128to256(\n")
            f.write("            U128 {\n")
            f.write(f"                high: {left_high}_u64,\n")
            f.write(f"                low: {left_low}_u64,\n")
            f.write("            },\n")
            f.write("            U128 {\n")
            f.write(f"                high: {right_high}_u64,\n")
            f.write(f"                low: {right_low}_u64,\n")
            f.write("            }\n")
            f.write("        ),\n")
            f.write("        U256 {\n")
            f.write("            high: U128 {\n")
            f.write(f"                high: {expected_high_high}_u64,\n")
            f.write(f"                low: {expected_high_low}_u64\n")
            f.write("            },\n")
            f.write("            low: U128 {\n")
            f.write(f"                high: {expected_low_high}_u64,\n")
            f.write(f"                low: {expected_low_low}_u64\n")
            f.write("            }\n")
            f.write("        }\n")
            f.write("    );\n")
    f.write("}\n")
    f.write("\n")
    f.write("#[test]\n")
    f.write("fn test_add256() {\n")
    for left in range(
        0,
        0x7777777777777777777777777777777777777777777777777777777777777777,
        0x2222222222222222222222222222222222222222222222222222222222222222,
    ):
        for right in range(
            0,
            0x7777777777777777777777777777777777777777777777777777777777777777,
            0x1111111111111111111111111111111111111111111111111111111111111111,
        ):
            expected = left + right
            expected_high = expected >> 128
            if expected_high & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF != expected_high:
                break
            left_high = left >> 128
            left_low = left & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            left_high_high = left_high >> 64
            left_high_low = left_high & 0xFFFFFFFFFFFFFFFF
            left_low_high = left_low >> 64
            left_low_low = left_low & 0xFFFFFFFFFFFFFFFF
            right_high = right >> 128
            right_low = right & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            right_high_high = right_high >> 64
            right_high_low = right_high & 0xFFFFFFFFFFFFFFFF
            right_low_high = right_low >> 64
            right_low_low = right_low & 0xFFFFFFFFFFFFFFFF
            expected_low = expected & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
            expected_high_high = expected_high >> 64
            expected_high_low = expected_high & 0xFFFFFFFFFFFFFFFF
            expected_low_high = expected_low >> 64
            expected_low_low = expected_low & 0xFFFFFFFFFFFFFFFF
            f.write("    assert_eq!(\n")
            f.write("        add256(\n")
            f.write("            U256 {\n")
            f.write("                high: U128 {\n")
            f.write(f"                    high: {left_high_high}_u64,\n")
            f.write(f"                    low: {left_high_low}_u64\n")
            f.write("                },\n")
            f.write("                low: U128 {\n")
            f.write(f"                    high: {left_low_high}_u64,\n")
            f.write(f"                    low: {left_low_low}_u64\n")
            f.write("                }\n")
            f.write("            },\n")
            f.write("            U256 {\n")
            f.write("                high: U128 {\n")
            f.write(f"                    high: {right_high_high}_u64,\n")
            f.write(f"                    low: {right_high_low}_u64\n")
            f.write("                },\n")
            f.write("                low: U128 {\n")
            f.write(f"                    high: {right_low_high}_u64,\n")
            f.write(f"                    low: {right_low_low}_u64\n")
            f.write("                }\n")
            f.write("            }\n")
            f.write("        ),\n")
            f.write("        U256 {\n")
            f.write("            high: U128 {\n")
            f.write(f"                high: {expected_high_high}_u64,\n")
            f.write(f"                low: {expected_high_low}_u64\n")
            f.write("            },\n")
            f.write("            low: U128 {\n")
            f.write(f"                high: {expected_low_high}_u64,\n")
            f.write(f"                low: {expected_low_low}_u64\n")
            f.write("            }\n")
            f.write("        }\n")
            f.write("    );\n")
    f.write("}\n")
