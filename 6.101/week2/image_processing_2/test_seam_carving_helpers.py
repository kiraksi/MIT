#!/usr/bin/env python3

import os
import lab
import types
import pickle
import hashlib
import collections

import pytest

from test import object_hash, compare_greyscale_images, compare_color_images, load_greyscale_image

TEST_DIRECTORY = os.path.dirname(__file__)

def test_pattern_greyscale():
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', 'pattern.png')
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    result = lab.greyscale_image_from_color_image(im)
    expected = {'height': 4, 
          'width': 9, 
          'pixels': [200, 160, 160, 160, 153, 160, 160, 160, 200, 
                     200, 160, 160, 160, 153, 160, 160, 160, 200, 
                       0, 153, 160, 160, 160, 160, 160, 153,  0, 
                       0, 153, 153, 160, 160, 160, 153, 153,  0]}
    assert object_hash(im)==oim, 'Be careful not to modify the original image!'
    compare_greyscale_images(result, expected)


def test_greyscale():
    for fname in ('centered_pixel', 'smallfrog', 'bluegill', 'twocats', 'tree'):
        inpfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{fname}.png')
        im = lab.load_color_image(inpfile)
        oim = object_hash(im)

        grey = lab.greyscale_image_from_color_image(im)
        expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_grey.png')
        assert object_hash(im) == oim, 'Be careful not to modify the original image!'
        compare_greyscale_images(grey, load_greyscale_image(expfile))


def test_pattern_energy():
    im = {'height': 4, 
          'width': 9, 
          'pixels': [200, 160, 160, 160, 153, 160, 160, 160, 200, 
                     200, 160, 160, 160, 153, 160, 160, 160, 200, 
                       0, 153, 160, 160, 160, 160, 160, 153,  0, 
                       0, 153, 153, 160, 160, 160, 153, 153,  0]}
    oim = object_hash(im)
    result = lab.compute_energy(im)
    expected = {
        'width': 9, 
        'height': 4, 
        'pixels': [160, 160,  0, 28,  0, 28,  0, 160, 160,
                   255, 218, 10, 22, 14, 22, 10, 218, 255, 
                   255, 255, 30,  0, 14,  0, 30, 255, 255, 
                   255, 255, 31, 22,  0, 22, 31, 255, 255]
    }
    assert object_hash(im)==oim, 'Be careful not to modify the original image!'
    compare_greyscale_images(result, expected)


def test_energy():
    for fname in ('centered_pixel', 'smallfrog', 'bluegill', 'twocats', 'tree'):
        inpfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{fname}.png')
        im = load_greyscale_image(inpfile)
        oim = object_hash(im)
        result = lab.compute_energy(im)
        assert object_hash(im) == oim, 'Be careful not to modify the original image!'

        expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_energy.pickle')
        with open(expfile, 'rb') as f:
            energy = pickle.load(f)

        compare_greyscale_images(result, energy)


def test_pattern_cumulative_energy():
    energy = {
        'width': 9, 
        'height': 4, 
        'pixels': [160, 160,  0, 28,  0, 28,  0, 160, 160,
                   255, 218, 10, 22, 14, 22, 10, 218, 255, 
                   255, 255, 30,  0, 14,  0, 30, 255, 255, 
                   255, 255, 31, 22,  0, 22, 31, 255, 255]
    }
    oim = object_hash(energy)
    result = lab.cumulative_energy_map(energy)
    expected = {
        'width': 9, 
        'height': 4, 
        'pixels': [160, 160,  0, 28,  0, 28,  0, 160, 160, 
                   415, 218, 10, 22, 14, 22, 10, 218, 415, 
                   473, 265, 40, 10, 28, 10, 40, 265, 473, 
                   520, 295, 41, 32, 10, 32, 41, 295, 520]
    }
    assert object_hash(energy)==oim, 'Be careful not to modify the original energy!'
    compare_greyscale_images(result, expected)


def test_cumulative_energy():
    for fname in ('centered_pixel', 'smallfrog', 'bluegill', 'twocats', 'tree'):
        infile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_energy.pickle')
        with open(infile, 'rb') as f:
            energy = pickle.load(f)
        result = lab.cumulative_energy_map(energy)

        expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_cumulative_energy.pickle')
        with open(expfile, 'rb') as f:
            cem = pickle.load(f)

        compare_greyscale_images(result, cem)

def test_pattern_seam_indices():
    cem = {
        'width': 9, 
        'height': 4, 
        'pixels': [160, 160,  0, 28,  0, 28,  0, 160, 160, 
                   415, 218, 10, 22, 14, 22, 10, 218, 415, 
                   473, 265, 40, 10, 28, 10, 40, 265, 473, 
                   520, 295, 41, 32, 10, 32, 41, 295, 520]
    }
    oim = object_hash(cem)
    result = lab.minimum_energy_seam(cem)
    expected = [2, 11, 21, 31]
    assert object_hash(cem)==oim, 'Be careful not to modify the original cumulative energy map!'
    assert (set(result)==set(expected))


def test_min_seam_indices():
    for fname in ('centered_pixel', 'smallfrog', 'bluegill', 'twocats', 'tree'):
        infile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_cumulative_energy.pickle')
        with open(infile, 'rb') as f:
            cem = pickle.load(f)
        result = lab.minimum_energy_seam(cem)

        expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_minimum_energy_seam.pickle')
        with open(expfile, 'rb') as f:
            seam = pickle.load(f)

        assert len(result) == len(seam)
        assert set(result) == set(seam)

def test_pattern_seam_removal():
    inpfile = os.path.join(TEST_DIRECTORY, 'test_images', 'pattern.png')
    im = lab.load_color_image(inpfile)
    oim = object_hash(im)
    seam_indices = [2, 11, 21, 31]
    result = lab.image_without_seam(im, seam_indices)
    expfile = os.path.join(TEST_DIRECTORY, 'test_results', 'pattern_1seam.png')
    assert object_hash(im)==oim, 'Be careful not to modify the original image!'
    compare_color_images(result, lab.load_color_image(expfile))


def test_seam_removal():
    for fname in ('pattern', 'bluegill', 'twocats', 'tree'):
        infile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_minimum_energy_seam.pickle')
        with open(infile, 'rb') as f:
            seam = pickle.load(f)

        imfile = os.path.join(TEST_DIRECTORY, 'test_images', f'{fname}.png')
        result = lab.image_without_seam(lab.load_color_image(imfile), seam)

        expfile = os.path.join(TEST_DIRECTORY, 'test_results', f'{fname}_1seam.png')
        compare_color_images(result, lab.load_color_image(expfile))


if __name__ == "__main__":
    import sys

    res = pytest.main(["-k", " or ".join(sys.argv[1:]), "-v", __file__])
