from crimson_trainer.offsets.loader import OffsetTable


def test_offset_table_loads():
    table = OffsetTable.load("1.4.2")
    assert table.build
    assert table.health > 0
    assert table.entity_stride >= 32