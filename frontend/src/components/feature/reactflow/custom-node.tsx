'use client';

import { useAtomValue } from 'jotai';
import Link from 'next/link';
import React, { useCallback, useState } from 'react';
import { Handle, NodeResizer, Position } from 'reactflow';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { showThemeAtom } from '@/lib/atoms/base';

interface IndustryClass {
  industryClassId: number;
  industryClassCode: number;
  industryClassName: string;
}

interface CustomNodeProps {
  data: {
    domainId: number;
    domainCode: number;
    domainName: string;
    classes: IndustryClass[];
    themes: IndustryClass[];
    contents: object[];
  };
  selected: boolean;
}
// 개별 industryClass 내용은 우선 contents에 저장 예정?

const CustomNode = ({ data, selected }: CustomNodeProps) => {
  const [nodeColor, setNodeColor] = useState('#fff');
  const showTheme = useAtomValue(showThemeAtom);
  const onChangeNodeColor = useCallback((event) => {
    setNodeColor(event.target.value);
  }, []);

  return (
    <div className="h-full">
      <NodeResizer isVisible={selected} minWidth={100} minHeight={30} />
      <Handle type="target" position={Position.Top} id="top" />
      <Handle type="target" position={Position.Right} id="right" />
      <Handle type="target" position={Position.Left} id="left" />
      <Handle type="target" position={Position.Bottom} id="bottom" />
      <Card className={`h-full box-border bg-[${nodeColor}]`}>
        <CardHeader className="w-full h-[64px]">
          <CardTitle>
            <span>{data.domainName}</span>
            <input
              className="nodrag h-full inline-flex ml-auto"
              type="color"
              onChange={onChangeNodeColor}
            />
          </CardTitle>
        </CardHeader>
        <CardContent className="overflow-y-auto h-[calc(100%-64px)]">
          <div>
            <p className="text-sm font-medium leading-none mb-2">Classes</p>
            <div className="flex flex-wrap gap-2">
              {data.classes.map((classItem, i) => (
                <Button asChild key={i}>
                  <Link href="#">
                    <div>{classItem.industryClassName}</div>
                  </Link>
                </Button>
              ))}
            </div>
          </div>
          {showTheme && (
            <div className="pt-4">
              <p className="text-sm font-medium leading-none mb-2">Themes</p>
              <div className="flex flex-wrap gap-2">
                {data.themes.map((themeItem, i) => (
                  <div
                    key={i}
                    className="
                      inline-flex items-center justify-center whitespace-nowrap
                      rounded-md text-sm font-medium h-9 px-4 py-2
                      bg-secondary text-secondary-foreground
                    "
                  >
                    {themeItem.industryClassName}
                  </div>
                ))}
              </div>
            </div>
          )}
        </CardContent>
      </Card>
      <Handle type="source" position={Position.Top} id="top" />
      <Handle type="source" position={Position.Right} id="right" />
      <Handle type="source" position={Position.Left} id="left" />
      <Handle type="source" position={Position.Bottom} id="bottom" />
    </div>
  );
};

export default CustomNode;
