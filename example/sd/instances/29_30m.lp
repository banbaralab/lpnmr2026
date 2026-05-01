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
required(  2, 10).
required(  3, 10).
required(  4, 10).
required(  5, 10).
required(  6, 10).
required(  7, 10).
required(  8, 15).
required(  9, 15).
required( 10, 19).
required( 11, 19).
required( 12, 20).
required( 13, 17).
required( 14, 19).
required( 15, 19).
required( 16, 22).
required( 17, 22).
required( 18, 22).
required( 19, 22).
required( 20, 22).
required( 21, 27).
required( 22, 27).
required( 23, 27).
required( 24, 20).
required( 25, 22).
required( 26, 21).
required( 27, 21).
required( 28, 17).
required( 29, 13).
required( 30, 16).
required( 31, 18).
required( 32, 17).
required( 33, 19).
required( 34, 17).
required( 35, 12).
required( 36, 12).
required( 37, 12).
required( 38, 12).
required( 39, 12).
required( 40, 16).
required( 41, 16).
required( 42, 17).
required( 43, 17).
required( 44, 20).
required( 45, 18).
required( 46, 18).
required( 47, 18).
required( 48, 18).
required( 49, 16).
required( 50, 14).
required( 51, 14).
required( 52, 14).
required( 53, 14).
required( 54, 14).
required( 55, 14).
required( 56, 19).
required( 57, 19).
required( 58, 23).
required( 59, 19).
required( 60, 20).
required( 61, 17).
required( 62, 15).
required( 63, 15).
required( 64, 19).
required( 65, 22).
required( 66, 22).
required( 67, 22).
required( 68, 22).
required( 69, 27).
required( 70, 27).
required( 71, 30).
required( 72, 23).
required( 73, 25).
required( 74, 24).
required( 75, 24).
required( 76, 20).
required( 77, 16).
required( 78, 19).
required( 79, 21).
required( 80, 20).
required( 81, 22).
required( 82, 20).
required( 83, 15).
required( 84, 15).
required( 85, 15).
required( 86, 15).
required( 87, 15).
required( 88, 19).
required( 89, 19).
required( 90, 20).
required( 91, 20).
required( 92, 24).
required( 93, 19).
required( 94, 19).
required( 95, 19).
required( 96, 19).
required( 97, 17).
required( 98, 15).
required( 99, 15).
required(100, 15).
required(101, 15).
required(102, 15).
required(103, 15).
required(104, 20).
required(105, 20).
required(106, 24).
required(107, 20).
required(108, 21).
required(109, 18).
required(110, 19).
required(111, 19).
required(112, 21).
required(113, 21).
required(114, 21).
required(115, 21).
required(116, 21).
required(117, 23).
required(118, 23).
required(119, 23).
required(120, 13).
required(121, 15).
required(122, 18).
required(123, 18).
required(124, 14).
required(125, 10).
required(126, 13).
required(127, 15).
required(128, 14).
required(129, 16).
required(130, 14).
required(131, 12).
required(132, 12).
required(133, 12).
required(134, 12).
required(135, 12).
required(136, 16).
required(137, 16).
required(138, 17).
required(139, 17).
required(140, 21).
required(141, 19).
required(142, 19).
required(143, 19).
required(144, 19).
required(145, 17).
required(146, 15).
required(147, 15).
required(148, 15).
required(149, 15).
required(150, 15).
required(151, 15).
required(152, 20).
required(153, 20).
required(154, 24).
required(155, 20).
required(156, 21).
required(157, 18).
required(158, 16).
required(159, 16).
required(160, 22).
required(161, 22).
required(162, 22).
required(163, 22).
required(164, 22).
required(165, 27).
required(166, 27).
required(167, 27).
required(168, 20).
required(169, 22).
required(170, 21).
required(171, 21).
required(172, 17).
required(173, 13).
required(174, 16).
required(175, 18).
required(176, 17).
required(177, 19).
required(178, 17).
required(179, 12).
required(180, 12).
required(181, 12).
required(182, 12).
required(183, 12).
required(184, 13).
required(185, 13).
required(186, 14).
required(187, 14).
required(188, 18).
required(189, 16).
required(190, 16).
required(191, 16).
required(192, 16).
required(193, 14).
required(194, 12).
required(195, 12).
required(196, 12).
required(197, 12).
required(198, 12).
required(199, 12).
required(200, 16).
required(201, 16).
required(202, 20).
required(203, 16).
required(204, 17).
required(205, 14).
required(206, 15).
required(207, 15).
required(208, 21).
required(209, 21).
required(210, 21).
required(211, 21).
required(212, 21).
required(213, 26).
required(214, 26).
required(215, 26).
required(216, 20).
required(217, 22).
required(218, 21).
required(219, 21).
required(220, 17).
required(221, 13).
required(222, 16).
required(223, 18).
required(224, 17).
required(225, 18).
required(226, 16).
required(227, 11).
required(228, 11).
required(229, 11).
required(230, 11).
required(231, 11).
required(232, 15).
required(233, 15).
required(234, 16).
required(235, 16).
required(236, 20).
required(237, 18).
required(238, 18).
required(239, 18).
required(240, 18).
required(241, 17).
required(242, 15).
required(243, 15).
required(244, 15).
required(245, 15).
required(246, 15).
required(247, 15).
required(248, 19).
required(249, 19).
required(250, 21).
required(251, 17).
required(252, 18).
required(253, 15).
required(254, 15).
required(255, 15).
required(256, 22).
required(257, 22).
required(258, 22).
required(259, 22).
required(260, 22).
required(261, 27).
required(262, 27).
required(263, 29).
required(264, 21).
required(265, 23).
required(266, 20).
required(267, 20).
required(268, 18).
required(269, 14).
required(270, 19).
required(271, 21).
required(272, 20).
required(273, 22).
required(274, 20).
required(275, 15).
required(276, 15).
required(277, 15).
required(278, 15).
required(279, 15).
required(280, 13).
required(281, 13).
required(282, 11).
required(283, 11).
required(284, 18).
required(285, 14).
required(286, 14).
required(287, 14).
required(288, 14).
required(289, 12).
required(290, 10).
required(291, 10).
required(292, 10).
required(293, 10).
required(294, 10).
required(295, 10).
required(296, 13).
required(297, 13).
required(298, 15).
required(299, 15).
required(300, 16).
required(301, 13).
required(302, 19).
required(303, 19).
required(304, 22).
required(305, 22).
required(306, 22).
required(307, 22).
required(308, 22).
required(309, 27).
required(310, 27).
required(311, 29).
required(312, 22).
required(313, 26).
required(314, 24).
required(315, 24).
required(316, 22).
required(317, 18).
required(318, 23).
required(319, 27).
required(320, 24).
required(321, 26).
required(322, 24).
required(323, 19).
required(324, 19).
required(325, 19).
required(326, 19).
required(327, 19).
required(328, 17).
required(329, 17).
required(330, 15).
required(331, 15).
required(332, 22).
required(333, 16).
required(334, 16).
required(335, 16).
