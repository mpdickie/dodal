import bluesky.plan_stubs as bps
import pytest
from bluesky import RunEngine

from dodal.devices.oav.oav_detector import OAV, ZoomController

TEST_GRID_TOP_LEFT_X = 100
TEST_GRID_TOP_LEFT_Y = 100
TEST_GRID_BOX_WIDTH = 25
TEST_GRID_NUM_BOXES_X = 5
TEST_GRID_NUM_BOXES_Y = 6


def take_snapshot_with_grid(oav: OAV, snapshot_filename, snapshot_directory):
    oav.wait_for_connection()
    yield from bps.abs_set(oav.snapshot.top_left_x, TEST_GRID_TOP_LEFT_X)
    yield from bps.abs_set(oav.snapshot.top_left_y, TEST_GRID_TOP_LEFT_Y)
    yield from bps.abs_set(oav.snapshot.box_width, TEST_GRID_BOX_WIDTH)
    yield from bps.abs_set(oav.snapshot.num_boxes_x, TEST_GRID_NUM_BOXES_X)
    yield from bps.abs_set(oav.snapshot.num_boxes_y, TEST_GRID_NUM_BOXES_Y)
    yield from bps.abs_set(oav.snapshot.filename, snapshot_filename)
    yield from bps.abs_set(oav.snapshot.directory, snapshot_directory)
    yield from bps.trigger(oav.snapshot, wait=True)


@pytest.mark.skip(reason="Don't want to actually take snapshots during testing.")
def test_grid_overlay():
    beamline = "BL03I"
    oav = OAV(name="oav", prefix=f"{beamline}-DI-OAV-01")
    snapshot_filename = "snapshot"
    snapshot_directory = "."
    RE = RunEngine()
    RE(take_snapshot_with_grid(oav, snapshot_filename, snapshot_directory))


@pytest.mark.skip(reason="No OAV in S03")
@pytest.mark.s03
def test_get_zoom_levels():
    my_zoom_controller = ZoomController("BL03S-EA-OAV-01:FZOOM:", name="test_zoom")
    my_zoom_controller.wait_for_connection()
    assert my_zoom_controller.allowed_zoom_levels[0] == "1.0x"
