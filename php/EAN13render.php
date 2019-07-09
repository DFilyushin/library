<?php

/**
 * EAN13 barcode renderer
 * Copyright 2012 Joel Yliluoma - http://iki.fi/bisqwit/
 * https://www.youtube.com/watch?v=5buJAAa_AX4
 */
class EAN13render
{
    // There are the different barcode patterns for each digit (7 bit each).
    // '1' represents a black line. '0' represents white (no line).
    static $Rcodes = Array('1110010', '1100110', '1101100', '1000010', '1011100',
                           '1001110', '1010000', '1000100', '1001000', '1110100');

    // The EAN13 defines three groups of bit patterns.
    // The 'R' pattern group, as above.
    // The 'G' group, which is a mirror of R (bits scanned in opposite order).
    // And the 'L' group, which is an inverse of R (0 becomes 1, 1 becomes 0).
    // Rather than defining them as arrays, we'll synthesize them at runtime.

    // This array describes whoch group to use for each digit,
    // depending on the first digit of the EAN code.
    static $groups = Array('LLLLLL', 'LLGLGG', 'LLGGLG', 'LLGGGL', 'LGLLGG',
                           'LGGLLG', 'LGGGLL', 'LGLGLG', 'LGLGGL', 'LGGLGL');

    public static function Render($barcode, $font)
    {
        $width = 123;
        $height = 78;
        $image = ImageCreateTrueColor($width, $height);
        imagefilledrectangle($image, 0, 0, $width, $height, 0xFFFFFF);
        $xpos = 19;

        // This function renders bit patterns.
        $synth = function($pattern, $transformation, $height) use (&$image, &$xpos)
        {
            $len = strlen($pattern);
            for ($i = 0; $i < $len; ++$i)
            {
                $index = $i;

                // If the group is 'G', mirror the code.
                if ($transformation == 'G') {
                    $index = ($len - 1) - $index;
                }

                // Choose the bit from the pattern.
                $bit = (int) $pattern[$index];

                // If the group is 'L', invert the bit.
                if ($transformation == 'L') {
                    $bit = 1 - $bit;
                }

                // If the group is '1', draw a vertical line in black color.
                if ($bit == 1) {
                    ImageLine($image, $xpos, 0, $xpos, $height, 0x000000);
                }

                ++$xpos;
            }
        };

        // Define the lengths of the barcode lines.
        $normal_height = $height - 12;
        $separator_height = $height - 7;
        
        // First, produce a begin separator (two thin bars).
        $synth('101', 'R', $separator_height);

        for ($n = 0; $n < 13; ++$n)
        {
            $digit = (int) $barcode[$n];

            if ($n == 0)
            {
                // Print the first digit separately (in black color)
                // Unless 0, which stands for UPC
                if ($digit != 0)
                {
                    ImageTTFtext($image, 8, 0, $xpos - 10, $height - 1, 0x000000, $font, $digit);
                }
            }
            else
            {
                // Print the digit (in black color)
                ImageTTFtext($image, 8, 0, $xpos, $height - 1, 0x000000, $font, $digit);

                // Produce the pattern
                $code = EAN13render::$Rcodes[$digit];
                $select = 'R';
                if ($n <= 6)
                {
                    // Choose the patterns for the left side digits based
                    // pn the first digit of the barcode
                    $select = EAN13render::$groups[ (int)$barcode[0] ][ $n - 1 ];
                }

                $synth($code, $select, $normal_height);

                if ($n == 6)
                {
                    // Produce the middle separator. Two thin bars, again.
                    $synth('01010', 'R', $separator_height);
                }
            }
        }

        // Last, produce the end separator
        // Which looks the same as the begin separator.
        $synth('101', 'R', $separator_height);

        return $image;
    }
}

putenv('GDFONTPATH=' . realpath('.'));

$barcode = '9788000007885';
//$barcode = sprintf('64%s', base_convert('BISQWIT', 36, 10));
$image = EAN13render::Render($barcode, 'arial');
ImagePng($image, 'test.png');
?>