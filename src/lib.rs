//! An assortment of prototype functions for adding and multiplying absurdly large numbers (128-bit and 256-bit).
//! THESE ARE NOT TO BE TREATED AS EXEMPLAR AND HAVE NOT BEEN THOROUGHLY CHECKED (e.g. there might be overflows, edge
//! cases, or whatever else)

// tests have a feature gate because it makes IDEs very slow
#[cfg(feature = "tests")]
mod tests;

#[derive(Default, Debug, PartialEq, Eq)]
pub struct U128 {
    high: u64,
    low: u64,
}

#[derive(Default, Debug, PartialEq, Eq)]
pub struct U256 {
    high: U128,
    low: U128,
}

pub fn mul64to128(a: u64, b: u64) -> U128 {
    // Adaptation of algorithm for multiplication of 32-bit unsigned integers described in Hacker's Delight by Henry S.
    // Warren, Jr. (ISBN 0-201-91465-4), Chapter 8. Basically, it's an optimized version of FOIL method applied to low
    // and high dwords of each operand.

    // Use 32-bit u32s to optimize the fallback for 32-bit platforms.
    let al = a as u32;
    let ah = (a >> 32) as u32;
    let bl = b as u32;
    let bh = (b >> 32) as u32;

    let mull = (al as u64) * (bl as u64);
    let t = (ah as u64) * (bl as u64) + (mull >> 32);
    let tl = (al as u64) * (bh as u64) + (t as u32 as u64);

    U128 {
        high: (ah as u64) * (bh as u64) + (t >> 32) + (tl >> 32),
        low: ((tl << 32) as u64) | (mull as u32 as u64),
    }
}

pub fn mul128(a: U128, b: U128) -> U128 {
    let mut ans = mul64to128(a.low, b.low);
    ans.high += (a.high * b.low) + (a.low * b.high);
    ans
}

pub fn add128(a: U128, b: U128) -> U128 {
    let carry = (((a.low & b.low) & 1) + (a.low >> 1) + (b.low >> 1)) >> 63;
    U128 {
        high: a.high + b.high + carry,
        low: a.low.wrapping_add(b.low), // a.low + b.low
    }
}

pub fn mul128to256(a: U128, b: U128) -> U256 {
    let mull = mul128(
        U128 {
            high: 0,
            low: a.low,
        },
        U128 {
            high: 0,
            low: b.low,
        },
    );
    let t = add128(
        mul128(
            U128 {
                high: 0,
                low: a.high,
            },
            U128 {
                high: 0,
                low: b.low,
            },
        ),
        U128 {
            high: 0,
            low: mull.high,
        },
    );
    let tl = add128(
        mul128(
            U128 {
                high: 0,
                low: a.low,
            },
            U128 {
                high: 0,
                low: b.high,
            },
        ),
        U128 {
            high: 0,
            low: t.low,
        },
    );
    let high = add128(
        mul128(
            U128 {
                high: 0,
                low: a.high,
            },
            U128 {
                high: 0,
                low: b.high,
            },
        ),
        add128(
            U128 {
                high: 0,
                low: t.high,
            },
            U128 {
                high: 0,
                low: tl.high,
            },
        ),
    );
    let low = U128 {
        high: tl.low,
        low: mull.low,
    };
    U256 { high, low }
}

pub fn add256(a: U256, b: U256) -> U256 {
    let carry = (((a.low.low & b.low.low) & 1) + (a.low.low >> 1) + (b.low.low >> 1)) >> 63;
    U256 {
        high: add128(
            a.high,
            add128(
                b.high,
                U128 {
                    high: 0,
                    low: carry,
                },
            ),
        ),
        low: add128(a.low, b.low),
    }
}
