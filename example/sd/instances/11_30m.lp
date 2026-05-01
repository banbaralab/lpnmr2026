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
required(  0, 10).
required(  1, 10).
required(  2, 10).
required(  3, 10).
required(  4, 10).
required(  5, 10).
required(  6, 10).
required(  7, 10).
required(  8, 10).
required(  9, 10).
required( 10,  7).
required( 11, 12).
required( 12, 12).
required( 13, 13).
required( 14,  8).
required( 15,  8).
required( 16, 10).
required( 17, 10).
required( 18, 12).
required( 19, 12).
required( 20, 12).
required( 21, 12).
required( 22, 12).
required( 23, 16).
required( 24, 15).
required( 25, 20).
required( 26, 20).
required( 27, 20).
required( 28, 20).
required( 29, 20).
required( 30, 22).
required( 31, 22).
required( 32, 22).
required( 33, 23).
required( 34, 23).
required( 35, 23).
required( 36, 23).
required( 37, 23).
required( 38, 23).
required( 39, 23).
required( 40, 24).
required( 41, 22).
required( 42, 22).
required( 43, 22).
required( 44, 17).
required( 45, 15).
required( 46, 15).
required( 47, 15).
required( 48, 14).
required( 49, 14).
required( 50, 14).
required( 51, 14).
required( 52, 14).
required( 53, 14).
required( 54, 14).
required( 55, 14).
required( 56, 14).
required( 57, 10).
required( 58,  7).
required( 59, 12).
required( 60, 12).
required( 61, 13).
required( 62,  8).
required( 63,  8).
required( 64, 10).
required( 65, 10).
required( 66, 13).
required( 67, 13).
required( 68, 13).
required( 69, 13).
required( 70, 13).
required( 71, 17).
required( 72, 16).
required( 73, 21).
required( 74, 23).
required( 75, 23).
required( 76, 23).
required( 77, 23).
required( 78, 24).
required( 79, 24).
required( 80, 24).
required( 81, 25).
required( 82, 25).
required( 83, 25).
required( 84, 25).
required( 85, 25).
required( 86, 25).
required( 87, 25).
required( 88, 25).
required( 89, 23).
required( 90, 23).
required( 91, 23).
required( 92, 18).
required( 93, 14).
required( 94, 14).
required( 95, 15).
required( 96, 14).
required( 97, 14).
required( 98, 14).
required( 99, 14).
required(100, 14).
required(101, 14).
required(102, 14).
required(103, 14).
required(104, 14).
required(105, 10).
required(106,  7).
required(107, 12).
required(108, 12).
required(109, 13).
required(110,  8).
required(111,  8).
required(112, 10).
required(113, 10).
required(114, 13).
required(115, 13).
required(116, 13).
required(117, 13).
required(118, 13).
required(119, 16).
required(120, 15).
required(121, 20).
required(122, 22).
required(123, 22).
required(124, 22).
required(125, 22).
required(126, 23).
required(127, 23).
required(128, 23).
required(129, 24).
required(130, 24).
required(131, 24).
required(132, 24).
required(133, 24).
required(134, 24).
required(135, 24).
required(136, 24).
required(137, 22).
required(138, 22).
required(139, 23).
required(140, 18).
required(141, 14).
required(142, 14).
required(143, 15).
required(144, 14).
required(145, 14).
required(146, 14).
required(147, 14).
required(148, 14).
required(149, 14).
required(150, 14).
required(151, 14).
required(152, 14).
required(153, 10).
required(154,  7).
required(155,  9).
required(156,  9).
required(157,  9).
required(158,  4).
required(159,  4).
required(160,  6).
required(161,  6).
required(162,  9).
required(163,  9).
required(164,  9).
required(165,  9).
required(166,  9).
required(167, 13).
required(168, 15).
required(169, 21).
required(170, 23).
required(171, 23).
required(172, 23).
required(173, 23).
required(174, 24).
required(175, 24).
required(176, 24).
required(177, 25).
required(178, 25).
required(179, 25).
required(180, 25).
required(181, 25).
required(182, 25).
required(183, 25).
required(184, 25).
required(185, 23).
required(186, 23).
required(187, 23).
required(188, 18).
required(189, 14).
required(190, 14).
required(191, 12).
required(192, 11).
required(193, 11).
required(194, 11).
required(195, 11).
required(196, 11).
required(197, 11).
required(198, 11).
required(199, 11).
required(200, 11).
required(201,  7).
required(202,  4).
required(203,  9).
required(204,  9).
required(205, 10).
required(206,  8).
required(207,  8).
required(208, 10).
required(209, 10).
required(210, 13).
required(211, 13).
required(212, 13).
required(213, 13).
required(214, 13).
required(215, 17).
required(216, 16).
required(217, 21).
required(218, 23).
required(219, 23).
required(220, 23).
required(221, 23).
required(222, 26).
required(223, 26).
required(224, 26).
required(225, 27).
required(226, 27).
required(227, 27).
required(228, 27).
required(229, 27).
required(230, 27).
required(231, 27).
required(232, 27).
required(233, 24).
required(234, 24).
required(235, 24).
required(236, 19).
required(237, 15).
required(238, 15).
required(239, 14).
required(240, 13).
required(241, 13).
required(242, 13).
required(243, 13).
required(244, 13).
required(245, 13).
required(246, 13).
required(247, 13).
required(248, 16).
required(249, 12).
required(250,  9).
required(251, 11).
required(252, 11).
required(253, 12).
required(254,  7).
required(255,  7).
required(256,  9).
required(257,  9).
required(258,  9).
required(259,  9).
required(260,  9).
required(261,  9).
required(262,  9).
required(263,  9).
required(264,  9).
required(265, 13).
required(266, 11).
required(267, 11).
required(268, 11).
required(269, 11).
required(270,  9).
required(271,  9).
required(272,  9).
required(273, 11).
required(274, 11).
required(275, 11).
required(276, 11).
required(277, 11).
required(278, 11).
required(279, 11).
required(280, 14).
required(281, 14).
required(282, 14).
required(283, 14).
required(284, 14).
required(285, 12).
required(286, 12).
required(287, 12).
required(288, 10).
required(289, 10).
required(290, 10).
required(291, 10).
required(292, 10).
required(293, 10).
required(294, 10).
required(295, 10).
required(296, 11).
required(297, 11).
required(298,  8).
required(299, 10).
required(300, 10).
required(301, 11).
required(302,  6).
required(303,  6).
required(304,  8).
required(305,  8).
required(306,  8).
required(307,  8).
required(308,  8).
required(309,  8).
required(310,  8).
required(311,  8).
required(312,  8).
required(313, 17).
required(314, 16).
required(315, 16).
required(316, 16).
required(317, 16).
required(318, 16).
required(319, 16).
required(320, 16).
required(321, 18).
required(322, 18).
required(323, 18).
required(324, 18).
required(325, 18).
required(326, 18).
required(327, 18).
required(328, 21).
required(329, 21).
required(330, 21).
required(331, 21).
required(332, 16).
required(333, 14).
required(334, 14).
required(335, 12).
