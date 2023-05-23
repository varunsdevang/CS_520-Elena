import { render, screen } from '@testing-library/react';
import React from "react";
import renderer from "react-test-renderer";
import ErrorDialog from '../Components/ErrorDialog';


describe("ErrorDialog snapshot should match", () => {
    it("Matches DOM Snapshot", () => {
      const domTree = renderer.create(< ErrorDialog/>).toJSON();
      expect(domTree).toMatchSnapshot();
    });
});