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
required(  0,  3).
required(  1,  3).
required(  2,  3).
required(  3,  3).
required(  4,  8).
required(  5,  8).
required(  6, 11).
required(  7, 11).
required(  8, 10).
required(  9, 10).
required( 10, 10).
required( 11, 10).
required( 12, 10).
required( 13, 10).
required( 14, 10).
required( 15, 10).
required( 16,  5).
required( 17,  5).
required( 18,  7).
required( 19,  7).
required( 20,  8).
required( 21,  8).
required( 22, 12).
required( 23, 12).
required( 24, 13).
required( 25, 13).
required( 26, 13).
required( 27, 13).
required( 28, 16).
required( 29, 16).
required( 30, 21).
required( 31, 21).
required( 32, 20).
required( 33, 20).
required( 34, 25).
required( 35, 25).
required( 36, 21).
required( 37, 21).
required( 38, 21).
required( 39, 21).
required( 40, 21).
required( 41, 21).
required( 42, 22).
required( 43, 22).
required( 44, 22).
required( 45, 22).
required( 46, 12).
required( 47, 12).
required( 48, 12).
required( 49, 12).
required( 50, 12).
required( 51, 12).
required( 52,  7).
required( 53,  7).
required( 54,  6).
required( 55,  6).
required( 56,  4).
required( 57,  4).
required( 58,  4).
required( 59,  4).
required( 60,  4).
required( 61,  4).
required( 62,  4).
required( 63,  4).
required( 64,  0).
required( 65,  0).
required( 66,  3).
required( 67,  3).
required( 68,  4).
required( 69,  4).
required( 70,  8).
required( 71,  8).
required( 72,  9).
required( 73,  9).
required( 74,  9).
required( 75,  9).
required( 76, 16).
required( 77, 16).
required( 78, 21).
required( 79, 21).
required( 80, 20).
required( 81, 20).
required( 82, 25).
required( 83, 25).
required( 84, 21).
required( 85, 21).
required( 86, 21).
required( 87, 21).
required( 88, 21).
required( 89, 21).
required( 90, 22).
required( 91, 22).
required( 92, 22).
required( 93, 22).
required( 94, 12).
required( 95, 12).
required( 96, 12).
required( 97, 12).
required( 98, 12).
required( 99, 12).
required(100,  8).
required(101,  8).
required(102,  7).
required(103,  7).
required(104,  5).
required(105,  5).
required(106,  5).
required(107,  5).
required(108,  5).
required(109,  5).
required(110,  5).
required(111,  5).
required(112,  1).
required(113,  1).
required(114,  4).
required(115,  4).
required(116,  5).
required(117,  5).
required(118,  9).
required(119,  9).
required(120, 10).
required(121, 10).
required(122, 10).
required(123, 10).
required(124, 16).
required(125, 16).
required(126, 21).
required(127, 21).
required(128, 20).
required(129, 20).
required(130, 25).
required(131, 25).
required(132, 21).
required(133, 21).
required(134, 21).
required(135, 21).
required(136, 21).
required(137, 21).
required(138, 22).
required(139, 22).
required(140, 22).
required(141, 22).
required(142, 12).
required(143, 12).
required(144, 12).
required(145, 12).
required(146, 12).
required(147, 12).
required(148, 12).
required(149, 12).
required(150, 11).
required(151, 11).
required(152,  9).
required(153,  9).
required(154,  9).
required(155,  9).
required(156,  9).
required(157,  9).
required(158,  9).
required(159,  9).
required(160,  5).
required(161,  5).
required(162,  8).
required(163,  8).
required(164,  9).
required(165,  9).
required(166, 13).
required(167, 13).
required(168, 14).
required(169, 14).
required(170, 14).
required(171, 14).
required(172, 16).
required(173, 16).
required(174, 21).
required(175, 21).
required(176, 20).
required(177, 20).
required(178, 25).
required(179, 25).
required(180, 21).
required(181, 21).
required(182, 21).
required(183, 21).
required(184, 21).
required(185, 21).
required(186, 22).
required(187, 22).
required(188, 22).
required(189, 22).
required(190, 12).
required(191, 12).
required(192, 12).
required(193, 12).
required(194, 12).
required(195, 12).
required(196, 12).
required(197, 12).
required(198, 11).
required(199, 11).
required(200,  9).
required(201,  9).
required(202,  9).
required(203,  9).
required(204,  9).
required(205,  9).
required(206,  9).
required(207,  9).
required(208,  5).
required(209,  5).
required(210,  8).
required(211,  8).
required(212, 13).
required(213, 13).
required(214, 17).
required(215, 17).
required(216, 18).
required(217, 18).
required(218, 18).
required(219, 18).
required(220, 20).
required(221, 20).
required(222, 21).
required(223, 21).
required(224, 20).
required(225, 20).
required(226, 25).
required(227, 25).
required(228, 21).
required(229, 21).
required(230, 21).
required(231, 21).
required(232, 21).
required(233, 21).
required(234, 22).
required(235, 22).
required(236, 22).
required(237, 22).
required(238, 12).
required(239, 12).
required(240, 12).
required(241, 12).
required(242, 12).
required(243, 12).
required(244,  8).
required(245,  8).
required(246,  7).
required(247,  7).
required(248,  5).
required(249,  5).
required(250,  5).
required(251,  5).
required(252,  5).
required(253,  5).
required(254,  5).
required(255,  5).
required(256,  1).
required(257,  1).
required(258,  6).
required(259,  6).
required(260,  7).
required(261,  7).
required(262, 10).
required(263, 10).
required(264, 11).
required(265, 11).
required(266, 11).
required(267, 11).
required(268,  9).
required(269,  9).
required(270, 14).
required(271, 14).
required(272, 13).
required(273, 13).
required(274, 15).
required(275, 15).
required(276, 12).
required(277, 12).
required(278, 12).
required(279, 12).
required(280, 12).
required(281, 12).
required(282, 12).
required(283, 12).
required(284, 12).
required(285, 12).
required(286,  3).
required(287,  3).
required(288,  3).
required(289,  3).
required(290,  3).
required(291,  3).
required(292,  4).
required(293,  4).
required(294,  6).
required(295,  6).
required(296,  5).
required(297,  5).
required(298,  5).
required(299,  5).
required(300,  5).
required(301,  5).
required(302,  5).
required(303,  5).
required(304,  1).
required(305,  1).
required(306,  6).
required(307,  6).
required(308,  7).
required(309,  7).
required(310, 10).
required(311, 10).
required(312, 11).
required(313, 11).
required(314, 11).
required(315, 11).
required(316,  9).
required(317,  9).
required(318, 14).
required(319, 14).
required(320, 13).
required(321, 13).
required(322, 15).
required(323, 15).
required(324, 12).
required(325, 12).
required(326, 12).
required(327, 12).
required(328, 12).
required(329, 12).
required(330, 12).
required(331, 12).
required(332, 12).
required(333, 12).
required(334,  3).
required(335,  3).
