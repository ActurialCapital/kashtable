import dateutil.parser


class ExcelFormatter:
    """
    Represents a styled table based on key elements located in an Excel spreadsheet.

    This class applies styling to a pandas DataFrame to represent it as a styled table. It utilizes
    the pandas styling functionality. For further information about the method used here, please 
    refer to the pandas styling documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html

    Attributes
    ----------
    uuid : str
        The UUID of the table.
    labels : str
        Description of labels.
    formatter : list
        List of formatting attributes.
    dt : list
        List of date columns.
    dt_formatted : list
        List of formatted date columns.
    attrs : str
        Attributes for the table HTML representation.
    df : pandas.DataFrame
        The DataFrame containing the table data.

    Methods
    -------
    _css_format(col, style)
        Apply CSS formatting to a column.
    _value_format(applied_to)
        Apply value formatting to specific columns.
    financials()
        Apply styling to the table for financial data.

    """

    def __init__(self, df, uuid='table1'):
        self.uuid = uuid
        self.labels = 'Description'
        self.formatter = [
            'table_name',
            'font_weight',
            'font_color',
            'background_color',
            'font_family',
            'font_size',
            'text_align',
            'sort_by'
        ]
        self.dt = list(
            df.loc[:, ~df.columns.isin(self.formatter)].drop(
                self.labels, axis=1)
            .columns
        )
        try:
            self.dt_formatted = [d.strftime("%b %Y") for d in self.dt]
        except:
            self.dt_formatted = [dateutil.parser.parse(
                d).strftime("%b %Y") for d in self.dt]
        self.attrs = 'class="table table-separate table-head-custom"'
        self.df = df.rename(columns=dict(zip(self.dt, self.dt_formatted)))
        self.df = self.df.dropna(axis=1, how='all')

    def _css_format(self, col, style):
        """
        Apply CSS formatting to a column.

        Parameters
        ----------
        col : str
            The column name.
        style : str
            The CSS style to apply.

        Returns
        -------
        function
            A lambda function for applying the CSS style.

        """
        return lambda x: ["{style}: {col}".format(style=style, col=x[col]) for _ in x]

    def _value_format(self, applied_to):
        """
        Apply value formatting to specific columns.

        Parameters
        ----------
        applied_to : list
            The list of columns to apply value formatting to.

        Returns
        -------
        dict
            A dictionary mapping column names to value formatting functions.

        """
        return dict(zip(applied_to, [lambda x: '{0:,.0f}'.format(x).replace(',', ' '
                                                                            ) if x >= 0 else '({0:,.0f})'.format(abs(x)).replace(',', ' ')] * len(applied_to)))

    def financials(self):
        """
        Apply styling to the table for financial data.

        Returns
        -------
        str
            The HTML representation of the styled table.

        """
        return (
            self.df.style
            .format(self._value_format(applied_to=self.dt_formatted), na_rep="-")
            .set_table_attributes(self.attrs)
            .apply(self._css_format(col='font_weight',      style='font-weight'), axis=1)
            .apply(self._css_format(col='font_weight',      style='font-style'), axis=1)
            .apply(self._css_format(col='font_color',       style='color'), axis=1)
            .apply(self._css_format(col='background_color', style='background-color'), axis=1)
            .apply(self._css_format(col='font_family',      style='font-family'), axis=1)
            .apply(self._css_format(col='font_size',        style='font-size'), axis=1)
            .apply(self._css_format(col='text_align',       style='text-align'), axis=1)
            .hide_index()
            .hide_columns(self.formatter)
            .render(uuid=self.uuid)
        )
