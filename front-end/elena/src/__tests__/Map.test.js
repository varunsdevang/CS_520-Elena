import { render, screen } from '@testing-library/react';
import React from "react";
import renderer from "react-test-renderer";
import Map from '../Components/Map';


describe("Map snapshot should match", () => {
    it("Matches DOM Snapshot", () => {
      const domTree = renderer.create(< Map/>).toJSON();
      expect(domTree).toMatchSnapshot();
    });
});