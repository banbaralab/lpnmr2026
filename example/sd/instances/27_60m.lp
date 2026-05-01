#const days = 7.
#const timeslots_per_day = 24.

% Name, Start, +Slots, -Slots
shift_start(m,  6, 2, 1).
shift_start(d, 10, 1, 1).
shift_start(e, 14, 1, 1).
shift_start(n, 22, 1, 1).

% Name, Length, +Slots, -Slots
shift_length(m, 8, 1, 1).
shift_length(d, 8, 1, 1).
shift_length(e, 8, 1, 1).
shift_length(n, 8, 1, 1).

% Define requirements for shifts
required(  0, 11).
required(  1, 11).
required(  2,  9).
required(  3,  5).
required(  4,  3).
required(  5,  3).
required(  6,  3).
required(  7,  2).
required(  8,  4).
required(  9,  5).
required( 10,  7).
required( 11, 12).
required( 12, 20).
required( 13, 23).
required( 14, 25).
required( 15, 31).
required( 16, 31).
required( 17, 25).
required( 18, 26).
required( 19, 24).
required( 20, 19).
required( 21, 21).
required( 22, 14).
required( 23, 15).
required( 24, 16).
required( 25, 16).
required( 26, 13).
required( 27,  5).
required( 28,  3).
required( 29,  3).
required( 30,  3).
required( 31,  2).
required( 32,  4).
required( 33,  6).
required( 34,  8).
required( 35, 13).
required( 36, 23).
required( 37, 23).
required( 38, 25).
required( 39, 26).
required( 40, 26).
required( 41, 19).
required( 42, 20).
required( 43, 18).
required( 44, 16).
required( 45, 18).
required( 46, 11).
required( 47, 12).
required( 48, 13).
required( 49, 13).
required( 50, 13).
required( 51,  5).
required( 52,  3).
required( 53,  3).
required( 54,  3).
required( 55,  2).
required( 56,  4).
required( 57,  5).
required( 58,  7).
required( 59, 12).
required( 60, 27).
required( 61, 27).
required( 62, 29).
required( 63, 27).
required( 64, 27).
required( 65, 21).
required( 66, 22).
required( 67, 20).
required( 68, 18).
required( 69, 20).
required( 70, 11).
required( 71, 12).
required( 72, 13).
required( 73, 13).
required( 74, 13).
required( 75,  5).
required( 76,  3).
required( 77,  3).
required( 78,  3).
required( 79,  2).
required( 80,  4).
required( 81,  5).
required( 82,  7).
required( 83, 12).
required( 84, 21).
required( 85, 21).
required( 86, 23).
required( 87, 28).
required( 88, 28).
required( 89, 22).
required( 90, 23).
required( 91, 21).
required( 92, 19).
required( 93, 21).
required( 94, 14).
required( 95, 15).
required( 96, 16).
required( 97, 16).
required( 98, 13).
required( 99,  5).
required(100,  3).
required(101,  3).
required(102,  3).
required(103,  2).
required(104,  4).
required(105,  5).
required(106,  7).
required(107, 12).
required(108, 20).
required(109, 20).
required(110, 22).
required(111, 25).
required(112, 25).
required(113, 19).
required(114, 20).
required(115, 18).
required(116, 16).
required(117, 18).
required(118, 11).
required(119, 12).
required(120, 12).
required(121, 12).
required(122, 12).
required(123,  6).
required(124,  4).
required(125,  4).
required(126,  2).
required(127,  2).
required(128,  7).
required(129,  8).
required(130, 10).
required(131, 15).
required(132, 24).
required(133, 24).
required(134, 29).
required(135, 30).
required(136, 30).
required(137, 28).
required(138, 29).
required(139, 24).
required(140, 22).
required(141, 18).
required(142, 12).
required(143, 10).
required(144, 10).
required(145, 10).
required(146,  8).
required(147,  8).
required(148,  6).
required(149,  6).
required(150,  2).
required(151,  2).
required(152,  4).
required(153,  5).
required(154,  7).
required(155, 12).
required(156, 21).
required(157, 21).
required(158, 26).
required(159, 27).
required(160, 27).
required(161, 25).
required(162, 28).
required(163, 26).
required(164, 24).
required(165, 20).
required(166, 14).
required(167, 10).
