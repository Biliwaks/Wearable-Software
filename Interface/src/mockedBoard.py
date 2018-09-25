# -*- coding: utf-8 -*-
"""A representation of the mocked physical board connected."""

from board import Board, Device

class MockedBoard(Board):
    """Representation of a mocked physical board."""

    def __init__(self):
        """Initialize the mocked board."""
        super().__init__()

        # Set custom values
        self._name = '<Mocked Board>'
        self._defaultIp = '0.0.0.0'
        self._defaultPort = '666'


        mockDevice = Device('Mock Device1')
        self._deviceList.append(mockDevice)

        mockDevice = Device('Mock Device2','out')
        self._deviceList.append(mockDevice)

        mockDevice = Device('Mock Device3','in',2)
        self._deviceList.append(mockDevice)

        mockDevice = Device('Mock Device4')
        self._deviceList.append(mockDevice)