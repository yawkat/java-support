#!/usr/bin/python3

import typing

import matplotlib

matplotlib.use("svg")

import matplotlib.axes
import matplotlib.image
import matplotlib.pyplot as plt
import matplotlib.text
import matplotlib.transforms


class SupportDate:
    def __init__(self, year: int, month: int, day: typing.Optional[int] = None):
        self.year = year
        self.month = month
        self.day = day

    def x_value(self, start) -> float:
        day = self.day
        if day is None:
            if start:
                day = 0
            else:
                day = 30
        return self.year + (self.month - 1) / 12 + day / 30 / 12


class Sdk:
    def __init__(self):
        sdk_list.append(self)
        self.tasks = []
        self.versions: typing.MutableSequence[str] = []

    def name(self, name: str, desc: str, detail: typing.Optional[str] = None, detail2: typing.Optional[str] = None):
        built = "$\\bf{%s}$ %s" % (name.replace(" ", "\\ "), desc)
        if detail:
            built += "\n" + detail
        if detail2:
            built += "\n$\default ^{%s}$" % detail2.replace(" ", "\\ ")

        self.title_height = len(built.split("\n")) * 0.2 + 0.4

        def upd(ax):
            ax.set_title(built, loc="left", pad=24)

        self.tasks.append(upd)

    def source(self, text: str, href: str):
        def work(ax):
            title = ax.set_title(text, loc="right", size="x-small", pad=24, color="#0000ff")
            title.set_url(href)

        self.tasks.append(work)

    def version_piece(self, version: str, fr: SupportDate, to: typing.Optional[SupportDate],
                      color: typing.Optional[str], text_in: typing.Optional[str] = None,
                      text_over: typing.Optional[str] = None):
        if version in self.versions:
            y = self.versions.index(version)
        else:
            y = len(self.versions)
            self.versions.append(version)
        fr_x = fr.x_value(start=True)
        if to is not None:
            to_x = to.x_value(start=False)
        else:
            to_x = fr_x + 0.1
            color = "#ffffff"
        self.tasks.append(lambda ax: ax.barh(y, to_x - fr_x, 0.5, left=fr_x, color=color))
        if text_in is not None:
            self.tasks.append(lambda ax: ax.annotate(text_in, (fr_x, y), verticalalignment="center", size="x-small"))
        if text_over is not None:
            self.tasks.append(
                lambda ax: ax.annotate(text_over, (fr_x, y - 0.5), verticalalignment="center", size="x-small",
                                       annotation_clip=False))

    def finish(self, x, y, width, height):
        ax: matplotlib.axes = plt.axes((x, y, width, height))
        ax.set_axisbelow(True)
        ax.set_xbound(2018, 2027)
        ax.set_autoscalex_on(False)
        ax.invert_yaxis()
        ax.set_xticks(list(range(2018, 2027)), minor=False)
        ax.set_xticks(list(map(lambda x: x + 0.5, range(2018, 2027))), minor=True)
        ax.set_xticklabels([], minor=False)
        ax.set_xticklabels(list(map(str, range(2018, 2027))), minor=True)
        for minor_tick in ax.xaxis.get_minor_ticks() + ax.xaxis.get_major_ticks():
            minor_tick.tick1line.set_markersize(0)
            minor_tick.tick2line.set_markersize(0)
        ax.grid(which="major", axis="x")

        for task in self.tasks:
            task(ax)

        ax.set_yticks(list(range(len(self.versions))))
        ax.set_yticklabels(self.versions)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.xaxis.tick_top()
        for major_tick in ax.yaxis.get_major_ticks():
            major_tick.tick1line.set_markersize(0)
            major_tick.tick2line.set_markersize(0)


sdk_count = 5
sdk_list: typing.MutableSequence[Sdk] = []

NORMAL = "#000000"
EXTENDED = "#808080"
UNSUPPORTED = "#b2b2b2"
NON_COMMERCIAL = "#e5e5e5"


def sts_support_range(release: int) -> typing.Tuple[SupportDate, SupportDate]:
    if release % 2 == 0:
        year = int(2018 + (release - 10) / 2)
        start = SupportDate(year, 3, 1)
        end = SupportDate(year, 9, 1)
    else:
        year = int(2017 + (release - 9) / 2)
        start = SupportDate(year, 9, 1)
        end = SupportDate(year + 1, 3, 1)
    return start, end


def is_lts(version):
    return version % 6 == 5


def _run():
    plt.rcParams['svg.fonttype'] = 'none'

    openjdk = Sdk()
    openjdk.name("OpenJDK", "is the GPL reference implementation of Java.",
                 r"LTS releases are not supported for longer than 6 months ${\it by\ oracle\ employees}$.",
                 "It is unclear who will support LTS under the OpenJDK umbrella for how long and if there will be official "
                 "builds.")
    openjdk.source("Change is the Only Constant with Mark Reinhold",
                   "https://www.youtube.com/watch?v=HqxZFoY_snQ")
    for i in range(9, 18):
        normal_start, normal_end = sts_support_range(i)
        openjdk.version_piece("%s" % i, normal_start, normal_end, color=NORMAL)

    oracle_free = Sdk()
    oracle_free.name("Oracle JDK (Free)", "is the JDK distribution by oracle.")
    oracle_free.source("Oracle Support Roadmap", "http://www.oracle.com/technetwork/java/eol-135779.html")
    oracle_free.version_piece("8", SupportDate(2019, 1, 15), SupportDate(2020, 12, 15), NON_COMMERCIAL,
                              text_over="non-corporate desktop use")
    oracle_free.version_piece("8", SupportDate(2014, 3, 15), SupportDate(2019, 1, 15), NORMAL)
    oracle_free.version_piece("9", SupportDate(2017, 9, 15), SupportDate(2018, 3, 15), NORMAL)
    oracle_free.version_piece("10", SupportDate(2018, 3, 15), SupportDate(2018, 9, 15), NORMAL)
    oracle_free.version_piece("11", SupportDate(2018, 9, 15), None, None, text_in="No Java 11 release")

    oracle_comm = Sdk()
    oracle_comm.name("Oracle JDK (Commercial)", "is the commercial JDK support by oracle.",
                     "LTS releases are supported for 5 years + 3 years extended + indefinite sustaining.")
    oracle_comm.source("Oracle Support Roadmap", "http://www.oracle.com/technetwork/java/eol-135779.html")
    for i in range(8, 18):
        normal_start, normal_end = sts_support_range(i)
        if i == 8:
            normal_end = SupportDate(2022, 3)
            lts = True
        elif is_lts(i):
            normal_end = SupportDate(normal_start.year + 5, normal_start.month)
            lts = True
        else:
            lts = False
        name = "%s" % i
        if lts:
            name = "LTS " + name
        oracle_comm.version_piece(name, normal_start, normal_end, color=NORMAL)
        if lts:
            oracle_comm.version_piece(name, normal_end, SupportDate(normal_end.year + 3, normal_end.month),
                                      color=EXTENDED)

    adopt = Sdk()
    adopt.name("AdoptOpenJDK", "is a community effort that provides free OpenJDK builds.",
               "LTS releases are supported for 4 years.")
    adopt.source("AdoptOpenJDK Support Roadmap", "https://adoptopenjdk.net/support.html")
    for i in range(8, 18):
        normal_start, normal_end = sts_support_range(i)
        name = str(i)
        if i == 8:
            name = "LTS 8"
            normal_end = SupportDate(2022, 9)
        elif is_lts(i):
            name = "LTS " + name
            normal_end = SupportDate(normal_start.year + 4, normal_start.month)
        adopt.version_piece(name, normal_start, normal_end, color=NORMAL)

    zulu_comm = Sdk()
    zulu_comm.name("Zulu Enterprise (Commercial)", "is the commercial JDK distribution by Azul.",
                   "MTS releases are supported for 18 months after the next LTS + 12 months extended\n"
                   "LTS releases are supported for 8 years + 2 years extended\n"
                   "Other releases are not supported, but builds are provided in Zulu community")
    zulu_comm.source("Zulu Enterprise OpenJDK Java Support Options",
                     "https://www.azul.com/products/zulu-and-zulu-enterprise/zulu-enterprise-java-support-options/")
    for i in range(8, 18):
        normal_start, normal_end = sts_support_range(i)
        extended_end = None
        if i == 8:
            normal_end = SupportDate(2025, 1)
            lts = True
            mts = False
        elif is_lts(i):
            normal_end = SupportDate(normal_start.year + 8, normal_start.month)
            extended_end = SupportDate(normal_end.year + 2, normal_end.month)
            lts = True
            mts = False
        elif i % 2 == 1:
            if is_lts(i + 2):
                normal_end = SupportDate(normal_start.year + 3, normal_start.month - 6)
            else:
                normal_end = SupportDate(normal_start.year + 4, normal_start.month - 6)
            extended_end = SupportDate(normal_end.year + 1, normal_end.month)
            lts = False
            mts = True
        else:
            lts = False
            mts = False
        name = "%s" % i
        if lts:
            name = "LTS " + name
        elif mts:
            name = "MTS " + name
        if lts or mts:
            if extended_end is not None:
                zulu_comm.version_piece(name, normal_end, extended_end, color=EXTENDED)
            zulu_comm.version_piece(name, normal_start, normal_end, color=NORMAL)
        else:
            zulu_comm.version_piece(name, normal_start, normal_end, color=UNSUPPORTED)

    heights = []
    for sdk in sdk_list:
        # extents = sdk.title.get_window_extent(plt.gcf().canvas.get_renderer())
        height = (sdk.title_height + len(sdk.versions) * 0.6) / 2
        heights.append(height)

    total_height = sum(heights) + 1
    plt.gcf().set_figwidth(9.81155)
    plt.gcf().set_figheight(total_height)

    plt.gcf().text(0, 1,
                   "Java Support Lifecycle\n",
                   verticalalignment="top",
                   fontsize=20)
    plt.gcf().text(0, (total_height - 0.35) / total_height,
                   "Oracle is changing its support policies for Oracle JDK and OpenJDK. In this Chart\n"
                   "alternate options for supported JDK distributions are shown.\n"
                   "$\\bf Horizontal\\ bars\\ represent\\ support\\ intervals.$",
                   verticalalignment="top")
    plt.gcf().text(1, 1,
                   "All information is liable to change.\nContact the particular vendors for details.",
                   verticalalignment="top", horizontalalignment="right")
    ccby_image = matplotlib.image.imread("https://licensebuttons.net/l/by/4.0/88x31.png")
    plt.gcf().figimage(ccby_image,
                       xo=plt.gcf().get_figwidth() * plt.gcf().dpi - ccby_image.shape[1],
                       yo=plt.gcf().get_figheight() * plt.gcf().dpi - ccby_image.shape[0] - 40).set_url(
        "https://creativecommons.org/licenses/by/4.0/")
    plt.gcf().text(1, (total_height - 0.775) / total_height,
                   "https://yawk.at/java-support/",
                   verticalalignment="top", horizontalalignment="right",
                   color="#0000ff"
                   ).set_url("https://yawk.at/java-support/")

    y = total_height - 1
    for sdk, height in zip(sdk_list, heights):
        y -= height
        sdk.finish(0.07, y / total_height, 1 - 0.07, (height - sdk.title_height) / total_height)

    #plt.show()
    plt.savefig("new-support.svg")


if __name__ == '__main__':
    _run()
