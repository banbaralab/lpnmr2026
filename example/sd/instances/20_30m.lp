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
required(  0, 11).
required(  1, 11).
required(  2, 11).
required(  3, 11).
required(  4, 11).
required(  5, 11).
required(  6, 13).
required(  7, 17).
required(  8, 17).
required(  9, 13).
required( 10, 12).
required( 11, 12).
required( 12, 12).
required( 13, 12).
required( 14, 10).
required( 15, 10).
required( 16, 10).
required( 17,  8).
required( 18,  8).
required( 19, 11).
required( 20, 13).
required( 21, 13).
required( 22, 14).
required( 23, 14).
required( 24, 18).
required( 25, 21).
required( 26, 21).
required( 27, 22).
required( 28, 22).
required( 29, 18).
required( 30, 21).
required( 31, 20).
required( 32, 20).
required( 33, 20).
required( 34, 20).
required( 35, 19).
required( 36, 19).
required( 37, 16).
required( 38, 16).
required( 39, 16).
required( 40, 20).
required( 41, 17).
required( 42, 13).
required( 43, 13).
required( 44, 13).
required( 45, 14).
required( 46, 18).
required( 47, 13).
required( 48, 13).
required( 49, 13).
required( 50, 13).
required( 51, 13).
required( 52, 13).
required( 53, 13).
required( 54, 17).
required( 55, 21).
required( 56, 21).
required( 57, 17).
required( 58, 12).
required( 59, 12).
required( 60, 12).
required( 61, 12).
required( 62, 12).
required( 63, 12).
required( 64, 12).
required( 65,  8).
required( 66,  8).
required( 67, 11).
required( 68, 13).
required( 69, 13).
required( 70, 14).
required( 71, 14).
required( 72, 18).
required( 73, 21).
required( 74, 21).
required( 75, 22).
required( 76, 22).
required( 77, 18).
required( 78, 21).
required( 79, 20).
required( 80, 20).
required( 81, 20).
required( 82, 20).
required( 83, 19).
required( 84, 19).
required( 85, 16).
required( 86, 16).
required( 87, 16).
required( 88, 20).
required( 89, 17).
required( 90, 13).
required( 91, 13).
required( 92, 13).
required( 93, 14).
required( 94, 18).
required( 95, 13).
required( 96, 13).
required( 97, 13).
required( 98, 13).
required( 99, 13).
required(100, 13).
required(101, 13).
required(102, 17).
required(103, 21).
required(104, 21).
required(105, 17).
required(106, 12).
required(107, 12).
required(108, 12).
required(109, 12).
required(110, 12).
required(111, 12).
required(112, 12).
required(113,  8).
required(114,  8).
required(115, 11).
required(116, 13).
required(117, 13).
required(118, 14).
required(119, 14).
required(120, 18).
required(121, 21).
required(122, 21).
required(123, 22).
required(124, 22).
required(125, 18).
required(126, 21).
required(127, 20).
required(128, 20).
required(129, 20).
required(130, 20).
required(131, 19).
required(132, 19).
required(133, 16).
required(134, 16).
required(135, 16).
required(136, 20).
required(137, 17).
required(138, 13).
required(139, 13).
required(140, 13).
required(141, 14).
required(142, 18).
required(143, 13).
required(144, 13).
required(145, 13).
required(146, 13).
required(147, 13).
required(148, 13).
required(149, 13).
required(150, 17).
required(151, 21).
required(152, 21).
required(153, 17).
required(154, 12).
required(155, 12).
required(156, 12).
required(157, 12).
required(158, 12).
required(159, 12).
required(160, 12).
required(161,  8).
required(162,  8).
required(163, 11).
required(164, 13).
required(165, 13).
required(166, 14).
required(167, 14).
required(168, 18).
required(169, 21).
required(170, 21).
required(171, 22).
required(172, 22).
required(173, 18).
required(174, 21).
required(175, 20).
required(176, 20).
required(177, 20).
required(178, 20).
required(179, 19).
required(180, 19).
required(181, 16).
required(182, 16).
required(183, 16).
required(184, 17).
required(185, 14).
required(186, 10).
required(187, 10).
required(188, 10).
required(189, 11).
required(190, 15).
required(191, 10).
required(192, 10).
required(193, 10).
required(194, 10).
required(195, 10).
required(196, 10).
required(197, 10).
required(198, 14).
required(199, 18).
required(200, 18).
required(201, 14).
required(202, 12).
required(203, 12).
required(204, 12).
required(205, 12).
required(206, 12).
required(207, 12).
required(208, 12).
required(209,  8).
required(210, 12).
required(211, 15).
required(212, 17).
required(213, 17).
required(214, 18).
required(215, 18).
required(216, 22).
required(217, 25).
required(218, 25).
required(219, 26).
required(220, 26).
required(221, 22).
required(222, 25).
required(223, 24).
required(224, 20).
required(225, 20).
required(226, 20).
required(227, 19).
required(228, 19).
required(229, 16).
required(230, 16).
required(231, 16).
required(232, 20).
required(233, 17).
required(234, 13).
required(235, 13).
required(236, 13).
required(237, 14).
required(238, 18).
required(239, 13).
required(240, 18).
required(241, 18).
required(242, 18).
required(243, 18).
required(244, 18).
required(245, 18).
required(246, 18).
required(247, 22).
required(248, 22).
required(249, 18).
required(250, 13).
required(251, 13).
required(252, 13).
required(253, 13).
required(254,  8).
required(255,  8).
required(256,  8).
required(257,  8).
required(258, 11).
required(259, 16).
required(260, 18).
required(261, 18).
required(262, 22).
required(263, 22).
required(264, 26).
required(265, 26).
required(266, 26).
required(267, 28).
required(268, 28).
required(269, 24).
required(270, 27).
required(271, 26).
required(272, 23).
required(273, 23).
required(274, 23).
required(275, 19).
required(276, 19).
required(277, 14).
required(278, 14).
required(279, 14).
required(280, 13).
required(281, 13).
required(282,  9).
required(283,  9).
required(284,  9).
required(285, 10).
required(286, 14).
required(287,  9).
required(288, 14).
required(289, 14).
required(290, 14).
required(291, 14).
required(292, 14).
required(293, 14).
required(294, 18).
required(295, 22).
required(296, 22).
required(297, 18).
required(298, 17).
required(299, 17).
required(300, 17).
required(301, 17).
required(302, 12).
required(303, 12).
required(304, 12).
required(305,  8).
required(306, 10).
required(307, 15).
required(308, 17).
required(309, 17).
required(310, 21).
required(311, 21).
required(312, 22).
required(313, 22).
required(314, 22).
required(315, 24).
required(316, 24).
required(317, 20).
required(318, 23).
required(319, 25).
required(320, 20).
required(321, 20).
required(322, 20).
required(323, 16).
required(324, 16).
required(325, 11).
required(326, 11).
required(327, 11).
required(328, 10).
required(329, 10).
required(330,  9).
required(331,  9).
required(332,  9).
required(333, 10).
required(334, 14).
required(335,  9).
