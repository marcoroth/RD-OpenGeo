import pytest

from geodata.models.imagery.etl import populate_image_entry
from . import factories
from .datastore import datastore


SampleFiles = [
    {'name': '20091021202517-01000100-VIS_0001.ntf', 'centroid': {'x': -84.1110, 'y': 39.781}},
    {'name': 'aerial_rgba_000003.tiff', 'centroid': {'x': -122.0050, 'y': 37.3359}},
    {'name': 'cclc_schu_100.tif', 'centroid': {'x': -76.8638, 'y': 42.3869}},
    {'name': 'landcover_sample_2000.tif', 'centroid': {'x': -75.4412, 'y': 42.6694}},
    {'name': 'paris_france_10.tiff', 'centroid': {'x': 2.5485, 'y': 49.0039}},
    {'name': 'rgb_geotiff.tiff', 'centroid': {'x': -117.1872, 'y': 33.1712}},
    {'name': 'RomanColosseum_WV2mulitband_10.tif', 'centroid': {'x': 12.4923, 'y': 41.8902}},
]

# These test files are dramatically downsampled for rapid testing
LandsatFiles = [
    'LC08_L1TP_034032_20200429_20200509_01_T1_sr_band1.tif',
    'LC08_L1TP_034032_20200429_20200509_01_T1_sr_band2.tif',
    'LC08_L1TP_034032_20200429_20200509_01_T1_sr_band3.tif',
]


@pytest.mark.parametrize('testfile', SampleFiles)
@pytest.mark.django_db(transaction=True)
def test_imagefile_to_rasterentry_centroids(testfile):
    imagefile = factories.ImageFileFactory(
        file__filename=testfile['name'], file__from_path=datastore.fetch(testfile['name']),
    )
    raster = factories.RasterEntryFactory(name=testfile['name'], images=[imagefile.imageentry.id])
    centroid = raster.footprint.centroid
    assert centroid.x == pytest.approx(testfile['centroid']['x'], abs=2e-4)
    assert centroid.y == pytest.approx(testfile['centroid']['y'], abs=2e-4)


@pytest.mark.django_db(transaction=True)
def test_repopulate_image_entry():
    """Only test with single image file."""
    testfile = SampleFiles[0]
    imagefile = factories.ImageFileFactory(
        file__filename=testfile['name'], file__from_path=datastore.fetch(testfile['name']),
    )
    # Testing that we can repopulate an image entry
    populate_image_entry(imagefile.id)


@pytest.mark.django_db(transaction=True)
def test_multi_file_raster():
    """Test the use case where a raster is generated from multiple files."""
    b1 = factories.ImageFileFactory(
        file__filename=LandsatFiles[0], file__from_path=datastore.fetch(LandsatFiles[0]),
    )
    b2 = factories.ImageFileFactory(
        file__filename=LandsatFiles[0], file__from_path=datastore.fetch(LandsatFiles[0]),
    )
    b3 = factories.ImageFileFactory(
        file__filename=LandsatFiles[0], file__from_path=datastore.fetch(LandsatFiles[0]),
    )
    # Create a RasterEntry from the three band image entries
    raster = factories.RasterEntryFactory(
        name='Multi File Test', images=[b1.imageentry.id, b2.imageentry.id, b3.imageentry.id]
    )
    assert raster.count == 3
    assert raster.crs is not None