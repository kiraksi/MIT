#!/usr/bin/env python3

import os
import lab
import types
import pickle
import hashlib
import collections

import pytest


TEST_DIRECTORY = os.path.dirname(__file__)


def object_hash(x):
    return hashlib.sha512(pickle.dumps(x)).hexdigest()


def compare_greyscale_images(im1, im2):
    assert set(im1.keys()) == {
        "height",
        "width",
        "pixels",
    }, "Incorrect keys in dictionary"
    assert im1["height"] == im2["height"], "Heights must match"
    assert im1["width"] == im2["width"], "Widths must match"
    assert (
        len(im1["pixels"]) == im1["height"] * im1["width"]
    ), "Incorrect number of pixels"
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1["pixels"], im2["pixels"])):
        assert (
            i == j
        ), "Incorrect value at location %s (differs from expected by %s)" % (
            ix,
            abs(i - j),
        )


def compare_color_images(im1, im2):
    assert set(im1.keys()) == {
        "height",
        "width",
        "pixels",
    }, "Incorrect keys in dictionary"
    assert im1["height"] == im2["height"], "Heights must match"
    assert im1["width"] == im2["width"], "Widths must match"
    assert (
        len(im1["pixels"]) == im1["height"] * im1["width"]
    ), "Incorrect number of pixels"
    assert all(
        isinstance(i, tuple) and len(i) == 3 for i in im1["pixels"]
    ), "Pixels must all be 3-tuples"
    assert all(
        0 <= subi <= 255 for i in im1["pixels"] for subi in i
    ), "Pixels values must all be in the range from [0, 255]"
    pix_incorrect = (None, None)
    for ix, (i, j) in enumerate(zip(im1["pixels"], im2["pixels"])):
        if i != j:
            assert (
                False
            ), "Incorrect value at location %s (differs from expected by %s)" % (
                ix,
                tuple(abs(i[t] - j[t]) for t in {0, 1, 2}),
            )


def test_load_color():
    result = lab.load_color_image("test_images/centered_pixel.png")
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [(244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (253, 253, 149), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198)]
    }
    compare_color_images(result, expected)


def test_color_filter_inverted():
    im = lab.load_color_image("test_images/centered_pixel.png")
    color_inverted = lab.color_filter_from_greyscale_filter(lab.inverted)
    assert callable(
        color_inverted
    ), "color_filter_from_greyscale_filter should return a function."
    result = color_inverted(im)
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [(11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),  (2, 2, 106), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57),
                   (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57), (11, 82, 57)]
    }
    compare_color_images(result, expected)


def test_color_filter_edges():
    im = lab.load_color_image("test_images/centered_pixel.png")
    color_edges = lab.color_filter_from_greyscale_filter(lab.edges)
    assert callable(
        color_edges
    ), "color_filter_from_greyscale_filter should return a function."
    result = color_edges(im)
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [(0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (13, 113, 69), (18, 160, 98), (13, 113, 69), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (18, 160, 98), (0, 0, 0), (18, 160, 98), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (13, 113, 69), (18, 160, 98), (13, 113, 69), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0),
                   (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0)],
    }
    compare_color_images(result, expected)


@pytest.mark.parametrize("fname", ["frog", "tree"])
@pytest.mark.parametrize("filter_name", ["edges", "inverted"])
def test_color_filter_images(fname, filter_name):
    filter_ = getattr(lab, filter_name)
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", f"{fname}.png")
    expfile = os.path.join(TEST_DIRECTORY, "test_results", f"{fname}_{filter_name}.png")
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    color_filter = lab.color_filter_from_greyscale_filter(filter_)
    assert callable(
        color_filter
    ), "color_filter_from_greyscale_filter should return a function."
    result = color_filter(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, "Be careful not to modify the original image!"
    compare_color_images(result, expected)


def test_blur_filter():
    blur_filter = lab.make_blur_filter(3)
    assert callable(blur_filter), "make_blur_filter should return a function."
    color_blur = lab.color_filter_from_greyscale_filter(blur_filter)
    im = lab.load_color_image("test_images/centered_pixel.png")
    result = color_blur(im)
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [(244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (245, 182, 193), (245, 182, 193), (245, 182, 193), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (245, 182, 193), (245, 182, 193), (245, 182, 193), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (245, 182, 193), (245, 182, 193), (245, 182, 193), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198),
                   (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198), (244, 173, 198)]
    }
    compare_color_images(result, expected)


@pytest.mark.parametrize("ker_size", [3, 5])
@pytest.mark.parametrize("fname", ["cat", "mushroom"])
def test_blur_filter_images(fname, ker_size):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", f"{fname}.png")
    expfile = os.path.join(
        TEST_DIRECTORY, "test_results", f"{fname}_blurred{ker_size}.png"
    )
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    blur_filter = lab.make_blur_filter(ker_size)
    assert callable(blur_filter), "make_blur_filter should return a function."
    color_blur = lab.color_filter_from_greyscale_filter(blur_filter)
    result = color_blur(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, "Be careful not to modify the original image!"
    compare_color_images(result, expected)


@pytest.mark.parametrize("ker_size", [3, 5])
@pytest.mark.parametrize("fname", ["construct", "bluegill"])
def test_sharpen_filter_images(fname, ker_size):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", f"{fname}.png")
    expfile = os.path.join(
        TEST_DIRECTORY, "test_results", f"{fname}_sharpened{ker_size}.png"
    )
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    sharpen_filter = lab.make_sharpen_filter(ker_size)
    assert callable(sharpen_filter), "make_sharpen_filter should return a function."
    color_sharpen = lab.color_filter_from_greyscale_filter(sharpen_filter)
    result = color_sharpen(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, "Be careful not to modify the original image!"
    compare_color_images(result, expected)


def test_small_cascade():
    color_edges = lab.color_filter_from_greyscale_filter(lab.edges)
    color_inverted = lab.color_filter_from_greyscale_filter(lab.inverted)
    color_blur_5 = lab.color_filter_from_greyscale_filter(lab.make_blur_filter(5))

    im = lab.load_color_image("test_images/centered_pixel.png")
    expected = {
        "height": 11,
        "width": 11,
        "pixels": [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 250, 252), (254, 244, 248), (253, 240, 246), (253, 240, 246), (253, 240, 246), (254, 244, 248), (254, 250, 252), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 244, 248), (253, 238, 244), (252, 227, 238), (252, 227, 238), (252, 227, 238), (253, 238, 244), (254, 244, 248), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (253, 240, 246), (252, 227, 238), (250, 211, 228), (250, 211, 228), (250, 211, 228), (252, 227, 238), (253, 240, 246), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (253, 240, 246), (252, 227, 238), (250, 211, 228), (250, 211, 228), (250, 211, 228), (252, 227, 238), (253, 240, 246), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (253, 240, 246), (252, 227, 238), (250, 211, 228), (250, 211, 228), (250, 211, 228), (252, 227, 238), (253, 240, 246), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 244, 248), (253, 238, 244), (252, 227, 238), (252, 227, 238), (252, 227, 238), (253, 238, 244), (254, 244, 248), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (254, 250, 252), (254, 244, 248), (253, 240, 246), (253, 240, 246), (253, 240, 246), (254, 244, 248), (254, 250, 252), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),
                   (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)]
    }
    f_cascade = lab.filter_cascade([color_edges, color_inverted, color_blur_5])
    assert callable(f_cascade), "filter_cascade should return a function."
    result = f_cascade(im)
    compare_color_images(result, expected)


@pytest.mark.parametrize("cascade", [0, 1, 2])
@pytest.mark.parametrize("image", ["tree", "stronger"])
def test_cascades(cascade, image):
    color_edges = lab.color_filter_from_greyscale_filter(lab.edges)
    color_inverted = lab.color_filter_from_greyscale_filter(lab.inverted)
    cascade0 = [
        color_edges,
        lab.color_filter_from_greyscale_filter(lab.make_sharpen_filter(3)),
    ]
    cascade1 = [
        lab.color_filter_from_greyscale_filter(lab.make_blur_filter(5)),
        color_edges,
        lab.color_filter_from_greyscale_filter(lab.make_sharpen_filter(3)),
        lambda im: {
            k: ([(i[1], i[0], i[2]) for i in v] if isinstance(v, list) else v)
            for k, v in im.items()
        },
    ]
    cascade2 = [color_edges] * 5 + [color_inverted]

    cascades = [cascade0, cascade1, cascade2]

    inpfile = os.path.join(TEST_DIRECTORY, "test_images", f"{image}.png")
    expfile = os.path.join(
        TEST_DIRECTORY, "test_results", f"{image}_cascade{cascade}.png"
    )
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    f_cascade = lab.filter_cascade(cascades[cascade])
    assert callable(f_cascade), "filter_cascade should return a function."
    result = f_cascade(im)
    expected = lab.load_color_image(expfile)
    assert object_hash(im) == oim, "Be careful not to modify the original image!"
    compare_color_images(result, expected)


def seams_endtoend(inp_name, out_name, number):
    inpfile = os.path.join(TEST_DIRECTORY, "test_images", inp_name)

    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    for i in range(1, number):
        result = lab.seam_carving(im, i)
        assert object_hash(im) == oim, "Be careful not to modify the original image!"

        expfile = os.path.join(TEST_DIRECTORY, "test_results", out_name, f"{i:02d}.png")
        compare_color_images(result, lab.load_color_image(expfile))


def seams_one(images):
    for i in images:
        inpfile = os.path.join(TEST_DIRECTORY, "test_images", f"{i}.png")
        im = lab.load_color_image(inpfile)

        oim = object_hash(im)
        result = lab.seam_carving(im, 1)
        assert object_hash(im) == oim, "Be careful not to modify the original image!"

        expfile = os.path.join(TEST_DIRECTORY, "test_results", f"{i}_1seam.png")
        compare_color_images(result, lab.load_color_image(expfile))


def test_seamcarving_images_1():
    seams_one(("pattern", "smallfrog"))


def test_seamcarving_images_2():
    seams_one(("bluegill", "tree", "twocats"))


def test_seamcarving_centeredpixel():
    seams_endtoend("centered_pixel.png", "seams_centered_pixel", 11)


def test_seamcarving_pattern():
    seams_endtoend("pattern.png", "seams_pattern", 9)


def test_seamcarving_smallfrog():
    seams_endtoend("smallfrog.png", "seams_smallfrog", 31)


def test_seamcarving_mushroom():
    seams_endtoend("smallmushroom.png", "seams_mushroom", 47)

def test_presence_of_custom_feature():
    assert hasattr(lab, 'custom_feature'), "Custom feature code is not present!"
    assert callable(lab.custom_feature), "custom_feature should be a function"

def load_greyscale_image(filename):
    """
    Loads an image from the given file and returns a dictionary
    representing that image.  This also performs conversion to greyscale.

    Invoked as, for example:
       i = load_image('test_images/cat.png')
    """
    from PIL import Image

    with open(filename, "rb") as img_handle:
        img = Image.open(img_handle)
        img_data = img.getdata()
        if img.mode.startswith("RGB"):
            pixels = [
                round(0.299 * p[0] + 0.587 * p[1] + 0.114 * p[2]) for p in img_data
            ]
        elif img.mode == "LA":
            pixels = [p[0] for p in img_data]
        elif img.mode == "L":
            pixels = list(img_data)
        else:
            raise ValueError("Unsupported image mode: %r" % img.mode)
        w, h = img.size
        return {"height": h, "width": w, "pixels": pixels}


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
