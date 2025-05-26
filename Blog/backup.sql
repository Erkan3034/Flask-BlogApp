-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 26, 2025 at 10:59 PM
-- Server version: 9.1.0
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `coder_erkan_blog`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int NOT NULL,
  `title` text NOT NULL,
  `author` text NOT NULL,
  `content` text CHARACTER SET utf32 COLLATE utf32_general_ci NOT NULL,
  `created_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_approved` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `title`, `author`, `content`, `created_date`, `is_approved`) VALUES
(1, 'İlk Makale', 'ErkanTrg', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a ullamcorper risus. Suspendisse turpis nisl, vestibulum ac laoreet quis, luctus ut sem. Cras malesuada tempus purus, ut convallis mauris aliquet eget. Pellentesque semper consectetur diam, in sodales eros iaculis a. Donec aliquet risus laoreet nibh semper, id mattis eros sollicitudin. Donec varius quis sapien id pulvinar. Nulla tempus ligula lorem, eget bibendum augue pulvinar id.', '2025-05-07 16:17:25', 1),
(2, 'Merhaba Flask Güncellendiiii', 'ErkanTrg', '<p><span style=\"font-family:\'Times New Roman\', Times, serif;\">Erkan Turgut. Bu senin ikinci Makale yazın.Makale Güncellendi!Erkan Turgut. Bu senin ikinci Makale yazın.Makale Güncellendi!Erkan Turgut. Bu senin ikinci Makale yazın.Makale Güncellendi!Erkan Turgut. Bu senin ikinci Makale yazın.Makale Güncellendi!</span></p>', '2025-05-07 20:46:22', 1),
(4, 'Spring Boot ile Hızlı Web Geliştirme', 'coder.zone', '<p>Spring Boot, Java ile web uygulamaları geliştirmeyi kolaylaştıran güçlü bir çerçevedir. Otomatik konfigürasyon ve gömülü sunucular sayesinde hızlı bir başlangıç sunar. REST API’lerden tam teşekküllü MVC uygulamalarına kadar geniş bir kullanım alanı sağlar. JPA ile veritabanı entegrasyonu, Spring Security ile güvenli uygulamalar ve mikroservis mimarisi desteği öne çıkar. Az kodla ölçeklenebilir ve bulut dostu uygulamalar geliştirmek isteyenler için ideal bir seçimdir. Başlamak için Spring Initializr’ı kullanabilirsiniz.</p>', '2025-05-07 21:41:12', 1),
(6, 'Yeni Makale', 'ErkanTrg', '<p><span style=\"color:hsl(240, 75%, 60%);\">Some quick example text to build on the card title and make up the bulk of the card\'s content.Some quick example text to build on the card title and make up the bulk of the card\'s content.Some quick example text to build on the card title and make up the bulk of the card\'s content.Some quick example text to build on the card title and make up the bulk of the card\'s content.</span></p>', '2025-05-09 11:13:17', 1),
(7, 'Css Position Ayarlama', 'ErkanTrg', '<p>position: absolute ile ikon input’un içine yerleştiriliyor.</p><p>right: 15px ile ikon input’un sağ tarafına yaslanıyor.</p><p>color: #333 → Siyahın açık tonu. Gerekirse #000 ile tam siyah yapabilirsin.</p><p>pointer-events: none → Tıklanamaz olur, böylece input kullanılabilir kalır.</p><p>pr-5 → Input içinde ikon için boşluk bırakır.</p><p><span style=\"color:hsl(120, 75%, 60%);\"><i><strong>Güncellendi</strong></i></span></p>', '2025-05-09 11:20:31', 1),
(8, 'Css-Bootstrap Search bar', 'ErkanTrg', '<p>Merhaba erkan</p>', '2025-05-09 11:23:58', 1),
(11, 'Code prettify kullanımı', 'ErkanTrg', '<p>Kullanım &ouml;rneği:</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<pre class=\"prettyprint\">class Voila {\r\npublic:\r\n  // Voila\r\n  static const string VOILA = \"Voila\";\r\n\r\n  // will not interfere with embedded <a href=\"#voila2\">tags</a>.\r\n}</pre>\r\n', '2025-05-09 12:12:59', 1),
(12, 'python Örnek Kodlar2', 'ErkanTrg', '<p>Kodlar:</p>\r\n\r\n<p>&nbsp;</p>\r\n\r\n<pre class=\"prettyprint\">\r\n@app.route(&quot;/search&quot;, methods=[&quot;GET&quot;, &quot;POST&quot;])\r\n@login_required # Kullanıcı giriş yapmamışsa login_required decoratoru ile y&ouml;nlendiriyoruz.\r\ndef search():\r\n    if request.method == &quot;POST&quot;:\r\n        keyword = request.form.get(&quot;keyword&quot;)\r\n        cursor = mysql.connection.cursor()  \r\n        search_query = &quot;SELECT * FROM articles WHERE title LIKE %s OR content LIKE %s&quot;\r\n        search_result = cursor.execute(search_query, (&#39;%&#39; + keyword + &#39;%&#39;, &#39;%&#39; + keyword + &#39;%&#39;))\r\n        if search_result &gt; 0:\r\n            articles = cursor.fetchall()\r\n            articles_list = list(articles)\r\n            articles_list.sort(key=lambda x: x[&#39;id&#39;], reverse=True)\r\n            return render_template(&quot;articles.html&quot;, articles=articles_list)\r\n        else:\r\n            flash(&quot;Aradığınız kelimeye uygun makale bulunamadı!&quot;, &quot;danger&quot;)\r\n            return redirect(url_for(&quot;index&quot;))\r\n            \r\n    elif request.method == &quot;GET&quot;:\r\n        return redirect(url_for(&quot;index&quot;))\r\n\r\n</pre>\r\n', '2025-05-09 12:15:41', 1),
(13, 'Örnek kullanıcı blogu', 'örnekk', '<p>Merhaba bu bir kullanıcı blogudur.</p>\r\n', '2025-05-09 15:18:09', 1),
(15, '10 Mayıs  2025 Tarihinde Gerçekleşen Olaylar.', 'ErkanTrg', '<p><a href=\"https://www.dodge.com/content/dam/fca-brands/na/dodge/en_us/wallpapers/desktop/2021/expanded/2021-dodge-wallpaper-challenger-06.jpg.image.1440.jpg\"><img alt=\"\" src=\"https://www.dodge.com/content/dam/fca-brands/na/dodge/en_us/wallpapers/desktop/2021/expanded/2021-dodge-wallpaper-challenger-06.jpg.image.1440.jpg\" style=\"width: 1036px; height: 500px;\" /></a>Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;Lorem ipsum dolor sit amet.&nbsp;</p>\r\n', '2025-05-10 16:26:44', 1);

-- --------------------------------------------------------

--
-- Table structure for table `navbar_links`
--

CREATE TABLE `navbar_links` (
  `id` int NOT NULL,
  `name` varchar(50) NOT NULL,
  `url` varchar(255) NOT NULL,
  `order_num` int DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `navbar_links`
--

INSERT INTO `navbar_links` (`id`, `name`, `url`, `order_num`) VALUES
(1, 'Linkedin', 'https://coderrzone.wasmer.app', 6);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `Id` int NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `userName` text NOT NULL,
  `password` text NOT NULL,
  `is_admin` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf32;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`Id`, `name`, `email`, `userName`, `password`, `is_admin`) VALUES
(4, 'Aslı Aydın', 'turguterkan15@gmail.com', 'mrx12', '$5$rounds=535000$bpreCId2nEG/IIs.$H3MGrSeWfSs6927GW8v4bYqqaKJD09zLGKjGlMJMF8/', 0),
(5, 'Serkan Turgut', 'Serkantrg56@gmail.com', 'serkan0101', '$5$rounds=535000$1DRLdzbtdmjuFh9X$iIL4vKJqNOMyruGZ07cornRr/9utzJqrrv593L.2Nc8', 0),
(6, 'coderr.zone', 'coderrzone55@gmail.com', 'coder12', '$5$rounds=535000$j/dYINAE4QS6Md1W$SYB4s4nka2Rah0j76wcdz0P6kVsd0VslqZ.TbzGYmo2', 0),
(7, 'Necip turgut', 'turguterkan30@gmail.com', 'Necip30', '$5$rounds=535000$8gTHuZO2CJVgwLoC$mIlKvlzvDFmq4nXZNJr5CeuJlydDu13Ak5iEn3Cfqh4', 0),
(8, 'Coder Erkan', 'coderrzone@gmail.com', 'cdrErkan', '$5$rounds=535000$uEuc9a9da9c.Tzac$klVqAnndKEBGeSZt9suY61vriU8P5rvsnKbDUA3.EG7', 0),
(9, 'Parsley Serif', 'abc@gmail.com', 'pasley', '$5$rounds=535000$XsWv.9S1RywNTekt$nuxAVF6L7uqQEyeTx.vCP6heuwWKGd.iHKMc0WaasV5', 0),
(10, 'Humphrey Shei', 'defs@gmail.com', 'humo', '$5$rounds=535000$LnQ9N1phUyI3PqYD$9FlJ20NrBmjm26pWgqhhUtNeWt2j3Z12nSmXZ/PhE54', 0),
(11, 'Doug Anthropy', 'dg55@gmail.com', 'doug', '$5$rounds=535000$z36.8YNvVGvmAoTW$iu26kF4dOIbV2ovcUPQSL3L0Rj43R2rd49/.3E5isu/', 0),
(12, 'Desmond Tone', 'desmo@gmail.com', 'desmo', '$5$rounds=535000$v88dvTXfBDq16PGV$sX9Z576.dnRb/D9bltyP/F6BOuD0Ggmeu4nWsxumRu0', 0),
(13, 'Lance Barrow', 'lancee@gmail.com', 'lanceiii', '$5$rounds=535000$eXmKXaVmPav/BK76$edw4rGSlCDKJdrtu.HvM6Edk7MvFJ7ia2.EOokvfCa9', 0),
(14, 'Fletch Saturation', 'fletch3@gmail.com', 'flet', '$5$rounds=535000$AspOUZIx13RrA.o/$UrMA4.ng1VVrYoiWAhakAFtiu6hUeQD4Vfy025woc/9', 0),
(15, 'Han Nutrisha', 'han@gmail.com', 'Hann', '$5$rounds=535000$Xc8HmQUQ6vKCVWew$aPqBQaYHKbJOILwQPlB7TMTgBPeuBJ8YBGTer3DfMa0', 0),
(16, 'Richard Skinner', 'rich@gmail.com', 'rich', '$5$rounds=535000$QFw.HjFk0Kc8lYaD$h05N9vqXsKhFDWz6R0whPOAfAJgLcGjrtsKiCseyfCC', 0),
(17, 'Thomas Meringue', 'thomas@gmail.com', 'Thomas', '$5$rounds=535000$Ch2311YiXMCG1MPL$pFMVU1fydppDGEnCIsBquYJewHlwqS0pFoZslnFp7TD', 0),
(18, 'Fleece Mann', 'flee@gmail.com', 'Flee', '$5$rounds=535000$NHD3za/S0yuUi54m$f.KKfiYczKAb/oq6mGyJM2ITFOYBgSjGS8.dervSzvA', 0),
(19, 'Piff Jenkins', 'piff@gmail.com', 'piff', '$5$rounds=535000$9BtTwtjjE7zom2GG$dZO836suz.nG9uy6.Bc.L7mw108LzifKCJkYlONk2sB', 0),
(20, 'Weir Doe', 'weir@gmail.com', 'weeir', '$5$rounds=535000$x5q12.NT2.2Vattn$EH914F/EmGJvsEy63PE3U3JuHbJs51IUasd.KIPhMI2', 0),
(21, 'Chaplain Mondover', 'Chaplain@gmail.com', 'Chaplain ', '$5$rounds=535000$nCqy4JQeim51iIwN$HmKD3giPPWtWpaidYohYExhPtcV7lkqd5euqZ2CH6J5', 0),
(22, 'Richard Tea', 'Richard@gmail.com', 'Richard', '$5$rounds=535000$mLZGj014Me9Dbgfx$a0hxLXueZJjgv5puQddEn87UhvZJoewuAyaqvm4w776', 0),
(23, 'Jarvis Pepperspray', 'Jarvis5@gmail.com', 'Jarvis ', '$5$rounds=535000$f5E9sy2vmW815qBs$s8qMA9R/WbdbPXJCSAvXQXrW5nBCKpNhgvZppw73cZ9', 0),
(24, 'Erkan Turgut ', 'turguterkan55@gmail.com', 'ErkanTrg', '$5$rounds=535000$.M2jI2YMnp9Tnuvr$yoQIS2RTOaC6H1U53iAl1tRiuzW2aYRKaHVETdLODP6', 1),
(25, 'Scott Chegg', 'Scott@gmail.com', 'Scott', '$5$rounds=535000$qusgw/tgLnLMxNiM$7j6tH48aReVYqllU8aNXiMAEdANGjnTMGNnkflXoNN8', 0),
(26, 'Hüseyin knk', 'hsyn@gmail.com', 'Hsyn_knk', '$5$rounds=535000$d7L8.dh9yeGgcmld$8VgqJQ0pP3Oh.S3hNtbgqGQWsKsCsMQRAd1tvtDP7e0', 0),
(27, 'Aslı Aslı', 'asliii@gmail.com', 'aslii', '$5$rounds=535000$IMcMUlaK/rPqFpuf$oj6Uy1oW8eY4IFoO45XwmqoQTLctA90YTqg6XwzL2oC', 0),
(28, 'coderr.zone', 'coderrzone1205@gmail.com', 'coder.zone', '$5$rounds=535000$p.np63AZ4f.I/T7V$8UU28txf2OIUHSY1oGsiR7VVz/FmLaqHc7Eg5A1huv5', 0),
(29, 'örnek', 'örnek@gmail.com', 'örnekk', '$5$rounds=535000$oZ7SWD1JEsda6gyE$8Tc0.RgC3IaSFKK/IH97xdKIGNj/rcmaKlCgKIZekF.', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `navbar_links`
--
ALTER TABLE `navbar_links`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`Id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `navbar_links`
--
ALTER TABLE `navbar_links`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `Id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
