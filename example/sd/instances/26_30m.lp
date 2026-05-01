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
required(  0, 16).
required(  1, 14).
required(  2, 14).
required(  3, 14).
required(  4, 14).
required(  5, 14).
required(  6, 14).
required(  7, 14).
required(  8, 20).
required(  9, 18).
required( 10, 19).
required( 11, 19).
required( 12, 19).
required( 13, 17).
required( 14, 16).
required( 15, 20).
required( 16, 20).
required( 17, 23).
required( 18, 23).
required( 19, 19).
required( 20, 22).
required( 21, 20).
required( 22, 19).
required( 23, 23).
required( 24, 28).
required( 25, 28).
required( 26, 33).
required( 27, 34).
required( 28, 29).
required( 29, 29).
required( 30, 29).
required( 31, 29).
required( 32, 25).
required( 33, 25).
required( 34, 25).
required( 35, 19).
required( 36, 19).
required( 37, 19).
required( 38, 13).
required( 39,  7).
required( 40,  9).
required( 41,  9).
required( 42,  9).
required( 43,  9).
required( 44,  9).
required( 45,  9).
required( 46,  9).
required( 47,  9).
required( 48, 16).
required( 49, 14).
required( 50, 14).
required( 51, 14).
required( 52, 14).
required( 53, 14).
required( 54, 14).
required( 55, 14).
required( 56, 20).
required( 57, 16).
required( 58, 17).
required( 59, 17).
required( 60, 17).
required( 61, 15).
required( 62, 14).
required( 63, 18).
required( 64, 18).
required( 65, 19).
required( 66, 19).
required( 67, 15).
required( 68, 16).
required( 69, 10).
required( 70,  9).
required( 71, 13).
required( 72, 18).
required( 73, 18).
required( 74, 23).
required( 75, 24).
required( 76, 21).
required( 77, 21).
required( 78, 23).
required( 79, 23).
required( 80, 19).
required( 81, 19).
required( 82, 19).
required( 83, 17).
required( 84, 17).
required( 85, 17).
required( 86, 13).
required( 87,  7).
required( 88,  9).
required( 89,  9).
required( 90,  9).
required( 91,  9).
required( 92,  9).
required( 93,  9).
required( 94,  9).
required( 95,  9).
required( 96, 18).
required( 97, 16).
required( 98, 16).
required( 99, 16).
required(100, 16).
required(101, 16).
required(102, 16).
required(103, 16).
required(104, 22).
required(105, 21).
required(106, 22).
required(107, 22).
required(108, 22).
required(109, 20).
required(110, 19).
required(111, 23).
required(112, 23).
required(113, 23).
required(114, 23).
required(115, 19).
required(116, 22).
required(117, 16).
required(118, 15).
required(119, 19).
required(120, 24).
required(121, 24).
required(122, 29).
required(123, 30).
required(124, 26).
required(125, 26).
required(126, 25).
required(127, 25).
required(128, 21).
required(129, 21).
required(130, 21).
required(131, 19).
required(132, 19).
required(133, 19).
required(134, 13).
required(135,  7).
required(136,  9).
required(137,  9).
required(138,  9).
required(139,  9).
required(140,  9).
required(141,  9).
required(142,  9).
required(143,  9).
required(144, 16).
required(145, 14).
required(146, 14).
required(147, 14).
required(148, 14).
required(149, 14).
required(150, 14).
required(151, 14).
required(152, 17).
required(153, 16).
required(154, 17).
required(155, 17).
required(156, 17).
required(157, 15).
required(158, 14).
required(159, 18).
required(160, 18).
required(161, 21).
required(162, 21).
required(163, 20).
required(164, 23).
required(165, 17).
required(166, 16).
required(167, 20).
required(168, 25).
required(169, 25).
required(170, 30).
required(171, 31).
required(172, 26).
required(173, 26).
required(174, 25).
required(175, 25).
required(176, 21).
required(177, 21).
required(178, 21).
required(179, 19).
required(180, 19).
required(181, 19).
required(182, 13).
required(183,  7).
required(184, 12).
required(185, 12).
required(186, 12).
required(187, 12).
required(188, 12).
required(189, 12).
required(190, 12).
required(191, 12).
required(192, 19).
required(193, 17).
required(194, 17).
required(195, 17).
required(196, 17).
required(197, 17).
required(198, 17).
required(199, 17).
required(200, 23).
required(201, 22).
required(202, 23).
required(203, 23).
required(204, 23).
required(205, 18).
required(206, 17).
required(207, 21).
required(208, 21).
required(209, 24).
required(210, 24).
required(211, 20).
required(212, 23).
required(213, 17).
required(214, 16).
required(215, 20).
required(216, 25).
required(217, 25).
required(218, 30).
required(219, 31).
required(220, 26).
required(221, 26).
required(222, 27).
required(223, 27).
required(224, 23).
required(225, 23).
required(226, 23).
required(227, 21).
required(228, 21).
required(229, 21).
required(230, 15).
required(231,  9).
required(232, 11).
required(233, 11).
required(234, 11).
required(235, 11).
required(236, 11).
required(237, 11).
required(238, 11).
required(239, 13).
required(240, 19).
required(241, 15).
required(242, 15).
required(243, 15).
required(244, 15).
required(245, 15).
required(246, 15).
required(247, 15).
required(248, 20).
required(249, 17).
required(250, 21).
required(251, 21).
required(252, 21).
required(253, 19).
required(254, 16).
required(255, 20).
required(256, 20).
required(257, 22).
required(258, 22).
required(259, 18).
required(260, 20).
required(261, 16).
required(262, 12).
required(263, 19).
required(264, 24).
required(265, 24).
required(266, 29).
required(267, 30).
required(268, 26).
required(269, 26).
required(270, 27).
required(271, 27).
required(272, 23).
required(273, 23).
required(274, 23).
required(275, 18).
required(276, 18).
required(277, 18).
required(278, 14).
required(279,  6).
required(280,  7).
required(281,  7).
required(282,  7).
required(283,  7).
required(284,  7).
required(285,  7).
required(286,  7).
required(287,  7).
required(288, 13).
required(289, 11).
required(290, 11).
required(291, 11).
required(292, 11).
required(293, 11).
required(294, 11).
required(295, 11).
required(296, 16).
required(297, 15).
required(298, 19).
required(299, 19).
required(300, 19).
required(301, 17).
required(302, 16).
required(303, 20).
required(304, 20).
required(305, 22).
required(306, 22).
required(307, 18).
required(308, 24).
required(309, 20).
required(310, 16).
required(311, 23).
required(312, 28).
required(313, 28).
required(314, 33).
required(315, 34).
required(316, 30).
required(317, 30).
required(318, 31).
required(319, 31).
required(320, 27).
required(321, 27).
required(322, 27).
required(323, 22).
required(324, 22).
required(325, 22).
required(326, 14).
required(327,  8).
required(328,  9).
required(329,  9).
required(330,  9).
required(331,  9).
required(332,  9).
required(333,  9).
required(334,  9).
required(335,  9).
