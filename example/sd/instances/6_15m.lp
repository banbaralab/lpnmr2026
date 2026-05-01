#const days = 7.
#const timeslots_per_day = 96.

% Name, Start, +Slots, -Slots
shift_start(m, 24, 8, 4).
shift_start(d, 40, 4, 4).
shift_start(e, 56, 4, 4).
shift_start(n, 88, 4, 4).

% Name, Length, +Slots, -Slots
shift_length(m, 32, 4, 4).
shift_length(d, 32, 4, 4).
shift_length(e, 32, 4, 4).
shift_length(n, 32, 4, 4).

% Define requirements for shifts
required(  0,  2).
required(  1,  2).
required(  2,  2).
required(  3,  2).
required(  4,  2).
required(  5,  2).
required(  6,  2).
required(  7,  2).
required(  8,  2).
required(  9,  2).
required( 10,  1).
required( 11,  1).
required( 12,  1).
required( 13,  1).
required( 14,  1).
required( 15,  1).
required( 16,  0).
required( 17,  0).
required( 18,  0).
required( 19,  0).
required( 20,  0).
required( 21,  0).
required( 22,  0).
required( 23,  0).
required( 24,  0).
required( 25,  1).
required( 26,  1).
required( 27,  1).
required( 28,  1).
required( 29,  1).
required( 30,  1).
required( 31,  1).
required( 32,  1).
required( 33,  2).
required( 34,  2).
required( 35,  2).
required( 36,  2).
required( 37,  2).
required( 38,  5).
required( 39,  5).
required( 40,  8).
required( 41,  8).
required( 42,  8).
required( 43,  8).
required( 44,  8).
required( 45,  8).
required( 46, 10).
required( 47, 10).
required( 48, 10).
required( 49, 10).
required( 50, 10).
required( 51, 10).
required( 52, 10).
required( 53, 10).
required( 54, 11).
required( 55, 11).
required( 56, 11).
required( 57, 11).
required( 58, 11).
required( 59, 12).
required( 60, 12).
required( 61, 12).
required( 62, 12).
required( 63, 13).
required( 64, 13).
required( 65, 13).
required( 66, 13).
required( 67, 13).
required( 68, 13).
required( 69, 13).
required( 70, 13).
required( 71, 11).
required( 72, 11).
required( 73, 11).
required( 74, 11).
required( 75, 11).
required( 76,  8).
required( 77,  8).
required( 78,  8).
required( 79,  8).
required( 80,  5).
required( 81,  5).
required( 82,  5).
required( 83,  5).
required( 84,  5).
required( 85,  5).
required( 86,  5).
required( 87,  5).
required( 88,  5).
required( 89,  4).
required( 90,  2).
required( 91,  2).
required( 92,  2).
required( 93,  2).
required( 94,  2).
required( 95,  2).
required( 96,  2).
required( 97,  2).
required( 98,  2).
required( 99,  2).
required(100,  2).
required(101,  2).
required(102,  2).
required(103,  2).
required(104,  2).
required(105,  2).
required(106,  1).
required(107,  1).
required(108,  1).
required(109,  1).
required(110,  1).
required(111,  1).
required(112,  0).
required(113,  0).
required(114,  0).
required(115,  0).
required(116,  0).
required(117,  0).
required(118,  0).
required(119,  0).
required(120,  0).
required(121,  1).
required(122,  1).
required(123,  1).
required(124,  1).
required(125,  1).
required(126,  1).
required(127,  1).
required(128,  1).
required(129,  2).
required(130,  2).
required(131,  2).
required(132,  2).
required(133,  2).
required(134,  4).
required(135,  4).
required(136,  4).
required(137,  4).
required(138,  4).
required(139,  4).
required(140,  4).
required(141,  4).
required(142,  5).
required(143,  5).
required(144,  5).
required(145,  5).
required(146,  5).
required(147,  5).
required(148,  5).
required(149,  5).
required(150,  6).
required(151,  6).
required(152,  6).
required(153,  6).
required(154,  6).
required(155,  7).
required(156,  7).
required(157,  7).
required(158,  7).
required(159,  8).
required(160,  8).
required(161,  8).
required(162,  8).
required(163,  8).
required(164,  8).
required(165,  8).
required(166,  8).
required(167,  7).
required(168,  7).
required(169,  7).
required(170,  7).
required(171,  7).
required(172,  5).
required(173,  5).
required(174,  5).
required(175,  5).
required(176,  5).
required(177,  5).
required(178,  5).
required(179,  5).
required(180,  5).
required(181,  5).
required(182,  5).
required(183,  5).
required(184,  5).
required(185,  4).
required(186,  2).
required(187,  2).
required(188,  2).
required(189,  2).
required(190,  2).
required(191,  2).
required(192,  2).
required(193,  2).
required(194,  2).
required(195,  2).
required(196,  2).
required(197,  2).
required(198,  2).
required(199,  2).
required(200,  2).
required(201,  2).
required(202,  1).
required(203,  1).
required(204,  1).
required(205,  1).
required(206,  1).
required(207,  1).
required(208,  0).
required(209,  0).
required(210,  0).
required(211,  0).
required(212,  0).
required(213,  0).
required(214,  0).
required(215,  0).
required(216,  0).
required(217,  1).
required(218,  1).
required(219,  1).
required(220,  1).
required(221,  1).
required(222,  1).
required(223,  1).
required(224,  1).
required(225,  2).
required(226,  2).
required(227,  2).
required(228,  2).
required(229,  2).
required(230,  5).
required(231,  5).
required(232,  5).
required(233,  5).
required(234,  5).
required(235,  5).
required(236,  5).
required(237,  5).
required(238,  7).
required(239,  7).
required(240,  7).
required(241,  7).
required(242,  7).
required(243,  7).
required(244,  7).
required(245,  7).
required(246,  8).
required(247,  8).
required(248,  8).
required(249,  8).
required(250,  8).
required(251,  9).
required(252,  9).
required(253,  9).
required(254,  9).
required(255, 10).
required(256, 10).
required(257, 10).
required(258, 10).
required(259, 10).
required(260, 10).
required(261, 10).
required(262, 10).
required(263,  8).
required(264,  8).
required(265,  8).
required(266,  8).
required(267,  8).
required(268,  5).
required(269,  5).
required(270,  5).
required(271,  5).
required(272,  5).
required(273,  5).
required(274,  5).
required(275,  5).
required(276,  5).
required(277,  5).
required(278,  5).
required(279,  5).
required(280,  5).
required(281,  4).
required(282,  2).
required(283,  2).
required(284,  2).
required(285,  2).
required(286,  2).
required(287,  2).
required(288,  2).
required(289,  2).
required(290,  2).
required(291,  2).
required(292,  2).
required(293,  2).
required(294,  2).
required(295,  2).
required(296,  2).
required(297,  2).
required(298,  1).
required(299,  1).
required(300,  1).
required(301,  1).
required(302,  1).
required(303,  1).
required(304,  0).
required(305,  0).
required(306,  0).
required(307,  0).
required(308,  0).
required(309,  0).
required(310,  0).
required(311,  0).
required(312,  0).
required(313,  1).
required(314,  1).
required(315,  1).
required(316,  1).
required(317,  1).
required(318,  1).
required(319,  1).
required(320,  1).
required(321,  2).
required(322,  2).
required(323,  2).
required(324,  2).
required(325,  2).
required(326,  5).
required(327,  5).
required(328,  8).
required(329,  8).
required(330,  8).
required(331,  8).
required(332,  8).
required(333,  8).
required(334, 10).
required(335, 10).
required(336, 10).
required(337, 10).
required(338, 10).
required(339, 10).
required(340, 10).
required(341, 10).
required(342, 11).
required(343, 11).
required(344, 11).
required(345, 11).
required(346, 11).
required(347, 12).
required(348, 12).
required(349, 12).
required(350, 12).
required(351, 13).
required(352, 13).
required(353, 13).
required(354, 13).
required(355, 13).
required(356, 13).
required(357, 13).
required(358, 13).
required(359, 11).
required(360, 11).
required(361, 11).
required(362, 11).
required(363, 11).
required(364,  8).
required(365,  8).
required(366,  8).
required(367,  8).
required(368,  5).
required(369,  5).
required(370,  5).
required(371,  5).
required(372,  5).
required(373,  5).
required(374,  5).
required(375,  5).
required(376,  5).
required(377,  4).
required(378,  2).
required(379,  7).
required(380,  7).
required(381,  7).
required(382,  7).
required(383,  7).
required(384,  7).
required(385,  7).
required(386,  7).
required(387,  7).
required(388,  7).
required(389,  7).
required(390,  7).
required(391,  7).
required(392,  7).
required(393,  7).
required(394,  6).
required(395,  6).
required(396,  6).
required(397,  6).
required(398,  6).
required(399,  6).
required(400,  5).
required(401,  5).
required(402,  5).
required(403,  5).
required(404,  5).
required(405,  5).
required(406,  5).
required(407,  6).
required(408,  6).
required(409,  7).
required(410,  7).
required(411,  7).
required(412,  7).
required(413,  7).
required(414,  2).
required(415,  2).
required(416,  2).
required(417,  3).
required(418,  3).
required(419,  3).
required(420,  3).
required(421,  3).
required(422,  6).
required(423,  6).
required(424,  9).
required(425,  9).
required(426,  9).
required(427,  9).
required(428,  9).
required(429,  9).
required(430, 11).
required(431, 11).
required(432, 11).
required(433, 11).
required(434, 11).
required(435, 11).
required(436, 11).
required(437, 10).
required(438, 11).
required(439, 11).
required(440, 11).
required(441, 11).
required(442, 11).
required(443, 12).
required(444, 12).
required(445, 12).
required(446, 12).
required(447, 13).
required(448, 13).
required(449, 13).
required(450, 13).
required(451, 13).
required(452, 13).
required(453, 13).
required(454, 13).
required(455, 11).
required(456, 11).
required(457, 11).
required(458, 11).
required(459, 11).
required(460,  8).
required(461,  8).
required(462,  8).
required(463,  8).
required(464,  5).
required(465,  5).
required(466,  5).
required(467,  5).
required(468,  5).
required(469,  5).
required(470,  5).
required(471,  5).
required(472,  5).
required(473,  4).
required(474,  2).
required(475,  2).
required(476,  2).
required(477,  2).
required(478,  2).
required(479,  2).
required(480,  2).
required(481,  2).
required(482,  2).
required(483,  2).
required(484,  2).
required(485,  2).
required(486,  2).
required(487,  2).
required(488,  2).
required(489,  2).
required(490,  1).
required(491,  1).
required(492,  1).
required(493,  1).
required(494,  1).
required(495,  1).
required(496,  0).
required(497,  0).
required(498,  0).
required(499,  0).
required(500,  0).
required(501,  0).
required(502,  0).
required(503,  4).
required(504,  4).
required(505,  5).
required(506,  5).
required(507,  5).
required(508,  5).
required(509,  5).
required(510,  5).
required(511,  5).
required(512,  5).
required(513,  6).
required(514,  6).
required(515,  6).
required(516,  6).
required(517,  6).
required(518, 10).
required(519, 10).
required(520, 13).
required(521, 13).
required(522, 13).
required(523, 13).
required(524, 13).
required(525, 13).
required(526, 15).
required(527, 15).
required(528, 15).
required(529, 15).
required(530, 15).
required(531, 15).
required(532, 15).
required(533, 11).
required(534, 15).
required(535, 15).
required(536, 15).
required(537, 15).
required(538, 15).
required(539, 18).
required(540, 18).
required(541, 18).
required(542, 18).
required(543, 18).
required(544, 18).
required(545, 18).
required(546, 18).
required(547, 18).
required(548, 18).
required(549, 18).
required(550, 18).
required(551, 16).
required(552, 16).
required(553, 16).
required(554, 16).
required(555, 16).
required(556, 12).
required(557, 12).
required(558, 12).
required(559, 12).
required(560,  9).
required(561,  9).
required(562,  6).
required(563,  6).
required(564,  6).
required(565,  6).
required(566,  6).
required(567,  6).
required(568,  6).
required(569,  3).
required(570,  2).
required(571,  2).
required(572,  2).
required(573,  2).
required(574,  2).
required(575,  2).
required(576,  2).
required(577,  2).
required(578,  2).
required(579,  2).
required(580,  2).
required(581,  2).
required(582,  2).
required(583,  2).
required(584,  2).
required(585,  2).
required(586,  1).
required(587,  1).
required(588,  1).
required(589,  1).
required(590,  1).
required(591,  1).
required(592,  0).
required(593,  0).
required(594,  0).
required(595,  0).
required(596,  0).
required(597,  0).
required(598,  0).
required(599,  4).
required(600,  4).
required(601,  5).
required(602,  5).
required(603,  5).
required(604,  5).
required(605,  5).
required(606,  5).
required(607,  5).
required(608,  5).
required(609,  6).
required(610,  6).
required(611,  6).
required(612,  6).
required(613,  6).
required(614,  7).
required(615,  7).
required(616, 10).
required(617, 10).
required(618, 10).
required(619, 10).
required(620, 10).
required(621, 10).
required(622, 12).
required(623, 12).
required(624, 12).
required(625, 12).
required(626, 12).
required(627, 12).
required(628, 12).
required(629,  8).
required(630, 12).
required(631, 12).
required(632, 12).
required(633, 12).
required(634, 12).
required(635, 14).
required(636, 14).
required(637, 14).
required(638, 14).
required(639, 14).
required(640, 14).
required(641, 14).
required(642, 14).
required(643, 14).
required(644, 14).
required(645, 14).
required(646, 14).
required(647, 12).
required(648, 12).
required(649, 12).
required(650, 12).
required(651, 12).
required(652, 11).
required(653, 11).
required(654, 11).
required(655, 11).
required(656,  8).
required(657,  8).
required(658,  5).
required(659,  5).
required(660,  5).
required(661,  5).
required(662,  5).
required(663,  5).
required(664,  5).
required(665,  3).
required(666,  2).
required(667,  2).
required(668,  2).
required(669,  2).
required(670,  2).
required(671,  2).
