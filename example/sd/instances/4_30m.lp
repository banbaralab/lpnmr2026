#const days = 7.
#const timeslots_per_day = 48.

% Name, Start, +Slots, -Slots
shift_start(m, 12, 4, 2).
shift_start(d, 20, 2, 2).
shift_start(e, 28, 2, 2).
shift_start(n, 44, 2, 2).

% Name, Length, +Slots, -Slots
shift_length(m, 16, 2, 2).
shift_length(d, 16, 2, 2).
shift_length(e, 16, 2, 2).
shift_length(n, 16, 2, 2).

% Define requirements for shifts
required(  0, 12).
required(  1, 12).
required(  2, 12).
required(  3, 12).
required(  4, 12).
required(  5, 12).
required(  6, 12).
required(  7, 12).
required(  8, 12).
required(  9, 12).
required( 10,  9).
required( 11, 10).
required( 12, 10).
required( 13, 10).
required( 14, 10).
required( 15, 10).
required( 16, 10).
required( 17, 16).
required( 18, 14).
required( 19, 14).
required( 20, 13).
required( 21, 13).
required( 22, 13).
required( 23, 16).
required( 24, 16).
required( 25, 16).
required( 26, 17).
required( 27, 18).
required( 28, 18).
required( 29, 18).
required( 30, 18).
required( 31, 18).
required( 32, 21).
required( 33, 21).
required( 34, 21).
required( 35, 21).
required( 36, 15).
required( 37, 12).
required( 38, 16).
required( 39, 16).
required( 40, 15).
required( 41, 15).
required( 42, 12).
required( 43,  8).
required( 44,  7).
required( 45,  7).
required( 46,  7).
required( 47,  7).
required( 48, 11).
required( 49, 11).
required( 50, 11).
required( 51, 11).
required( 52, 11).
required( 53, 11).
required( 54, 11).
required( 55, 11).
required( 56, 11).
required( 57, 11).
required( 58,  6).
required( 59,  7).
required( 60,  7).
required( 61,  7).
required( 62,  7).
required( 63,  7).
required( 64,  7).
required( 65, 13).
required( 66, 14).
required( 67, 14).
required( 68, 13).
required( 69, 13).
required( 70, 13).
required( 71, 16).
required( 72, 16).
required( 73, 16).
required( 74, 17).
required( 75, 18).
required( 76, 18).
required( 77, 18).
required( 78, 18).
required( 79, 18).
required( 80, 21).
required( 81, 21).
required( 82, 21).
required( 83, 21).
required( 84, 15).
required( 85, 12).
required( 86, 16).
required( 87, 16).
required( 88, 15).
required( 89, 15).
required( 90, 12).
required( 91,  8).
required( 92,  7).
required( 93,  7).
required( 94,  7).
required( 95,  7).
required( 96, 11).
required( 97, 11).
required( 98, 11).
required( 99, 11).
required(100, 11).
required(101, 11).
required(102, 11).
required(103, 11).
required(104, 11).
required(105, 11).
required(106,  6).
required(107,  7).
required(108,  7).
required(109,  7).
required(110,  7).
required(111,  7).
required(112,  7).
required(113, 13).
required(114, 14).
required(115, 14).
required(116, 13).
required(117, 13).
required(118, 13).
required(119, 16).
required(120, 16).
required(121, 16).
required(122, 17).
required(123, 18).
required(124, 18).
required(125, 18).
required(126, 18).
required(127, 18).
required(128, 21).
required(129, 21).
required(130, 21).
required(131, 21).
required(132, 15).
required(133, 12).
required(134, 16).
required(135, 16).
required(136, 15).
required(137, 15).
required(138, 12).
required(139,  8).
required(140,  7).
required(141,  7).
required(142,  7).
required(143,  7).
required(144, 11).
required(145, 11).
required(146, 11).
required(147, 11).
required(148, 11).
required(149, 11).
required(150, 11).
required(151, 11).
required(152, 11).
required(153, 11).
required(154,  6).
required(155,  7).
required(156,  7).
required(157,  7).
required(158,  7).
required(159,  7).
required(160,  7).
required(161, 13).
required(162, 14).
required(163, 14).
required(164, 13).
required(165, 13).
required(166, 13).
required(167, 16).
required(168, 16).
required(169, 16).
required(170, 17).
required(171, 17).
required(172, 17).
required(173, 17).
required(174, 17).
required(175, 17).
required(176, 20).
required(177, 20).
required(178, 20).
required(179, 20).
required(180, 14).
required(181, 11).
required(182, 16).
required(183, 16).
required(184, 15).
required(185, 15).
required(186, 12).
required(187,  8).
required(188,  7).
required(189,  7).
required(190,  7).
required(191,  7).
required(192, 11).
required(193, 11).
required(194, 11).
required(195, 11).
required(196, 11).
required(197, 11).
required(198, 11).
required(199, 11).
required(200, 11).
required(201, 11).
required(202,  6).
required(203,  7).
required(204,  7).
required(205,  7).
required(206,  7).
required(207,  7).
required(208,  7).
required(209, 13).
required(210, 14).
required(211, 14).
required(212, 13).
required(213, 13).
required(214, 13).
required(215, 16).
required(216, 16).
required(217, 16).
required(218, 18).
required(219, 19).
required(220, 19).
required(221, 19).
required(222, 19).
required(223, 19).
required(224, 22).
required(225, 22).
required(226, 22).
required(227, 22).
required(228, 16).
required(229, 13).
required(230, 17).
required(231, 17).
required(232, 15).
required(233, 15).
required(234, 12).
required(235,  8).
required(236,  7).
required(237,  7).
required(238,  7).
required(239,  7).
required(240, 10).
required(241, 10).
required(242, 10).
required(243, 10).
required(244, 10).
required(245, 10).
required(246, 10).
required(247, 10).
required(248, 10).
required(249, 10).
required(250,  5).
required(251,  6).
required(252,  6).
required(253,  6).
required(254,  6).
required(255,  6).
required(256,  6).
required(257, 15).
required(258, 14).
required(259, 14).
required(260, 14).
required(261, 14).
required(262, 14).
required(263, 19).
required(264, 19).
required(265, 19).
required(266, 19).
required(267, 24).
required(268, 24).
required(269, 24).
required(270, 24).
required(271, 24).
required(272, 26).
required(273, 26).
required(274, 26).
required(275, 26).
required(276, 20).
required(277, 16).
required(278, 14).
required(279, 14).
required(280, 14).
required(281, 14).
required(282, 11).
required(283,  8).
required(284,  8).
required(285,  8).
required(286,  8).
required(287,  8).
required(288, 11).
required(289, 11).
required(290, 11).
required(291, 11).
required(292, 11).
required(293, 11).
required(294, 11).
required(295, 11).
required(296, 11).
required(297, 11).
required(298,  8).
required(299,  9).
required(300,  9).
required(301,  9).
required(302,  9).
required(303,  9).
required(304,  9).
required(305, 18).
required(306, 14).
required(307, 14).
required(308, 14).
required(309, 14).
required(310, 14).
required(311, 19).
required(312, 19).
required(313, 19).
required(314, 19).
required(315, 23).
required(316, 23).
required(317, 23).
required(318, 23).
required(319, 23).
required(320, 25).
required(321, 25).
required(322, 25).
required(323, 25).
required(324, 19).
required(325, 15).
required(326, 14).
required(327, 14).
required(328, 14).
required(329, 14).
required(330, 11).
required(331,  8).
required(332,  8).
required(333,  8).
required(334,  8).
required(335,  8).
