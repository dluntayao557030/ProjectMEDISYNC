from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, Qt, QDate
from PyQt6.QtGui import QFont, QPixmap, QColor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QVBoxLayout, QTableWidget,
    QHeaderView, QComboBox, QDateEdit, QTextEdit, QPlainTextEdit, QTableWidgetItem, QAbstractItemView
)
class Designer:
    """
    The Designer class provides reusable UI builder utilities
    for creating styled PyQt6 widgets used throughout the project.
    It centralizes styling and layout logic to reduce repetitive code.
    """

    # -----------------------------------------------------------
    # WINDOW UTILITIES
    # -----------------------------------------------------------

    @staticmethod
    def setWindowToCenter(widget: QWidget):
        """
        Positions the given window at the center of the user's screen.

        Parameters:
            widget (QWidget): The window to be centered.
        """
        screen = QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        window_geometry = widget.frameGeometry()

        # Compute centered screen coordinates
        x = (screen_geometry.width() - window_geometry.width()) // 2
        y = (screen_geometry.height() - window_geometry.height()) // 2

        widget.move(x, y)

    # -----------------------------------------------------------
    # LABEL FACTORY
    # -----------------------------------------------------------

    @staticmethod
    def createLabel(text, parent, color, fontWeight, fontSize):
        """
        Creates a styled QLabel using the 'Lato' font.

        Parameters:
            text (str): The text displayed on the label.
            parent (QWidget | str): Parent widget, or "N/A" for no parent.
            color (str): CSS color value.
            fontWeight (int): CSS font-weight (e.g., 400, 700).
            fontSize (int): Font size in pixels.

        Returns:
            QLabel: The styled label widget.
        """
        label = QLabel(text) if parent == "N/A" else QLabel(text, parent)

        # Apply styling using CSS
        label.setStyleSheet(f"""
            QLabel {{
                color: {color};
                font-weight: {fontWeight};
                font-family: 'Lato';
                font-size: {fontSize}px;
            }}
        """)

        # Apply fallback QFont to ensure 'Lato' loads
        label.setFont(QFont("Lato", fontSize))
        return label

    # -----------------------------------------------------------
    # INPUT FIELD FACTORY
    # -----------------------------------------------------------

    @staticmethod
    def createInputField(
        parent, backgroundColor, fontColor, fontWeight, fontSize,
        borderRadius=0, outlineWeight=0, outlineColor=None
    ):
        """
        Creates a styled QLineEdit input field.

        Parameters:
            parent (QWidget): Parent widget.
            backgroundColor (str): Background color.
            fontColor (str): Text color.
            fontWeight (int): CSS font-weight.
            fontSize (int): Font size.
            borderRadius (int): Rounded corner radius.
            outlineWeight (int): Border width.
            outlineColor (str): Border color (optional).

        Returns:
            QLineEdit: The styled input field.
        """
        inputField = QLineEdit(parent)

        # Outline logic
        border_css = f"{outlineWeight}px solid {outlineColor}" if outlineWeight and outlineColor else "none"

        inputField.setStyleSheet(f"""
            QLineEdit {{
                background-color: {backgroundColor};
                color: {fontColor};
                font-weight: {fontWeight};
                font-family: 'Lato';
                font-size: {fontSize}px;
                border-radius: {borderRadius}px;
                border: {border_css};
            }}
        """)

        inputField.setFont(QFont("Lato", fontSize))
        return inputField

    @staticmethod
    def createPlainTextArea(parent, backgroundColor="white", fontColor="#333333",
                            fontSize=14, borderRadius=10, outlineWeight=2, outlineColor="#185777"):
        """
        Creates a styled QPlainTextEdit with a rounded card behind it to simulate border and rounded corners.

        Parameters:
            parent (QWidget): Parent widget.
            backgroundColor (str): Background color of the text area.
            fontColor (str): Text color.
            fontSize (int): Font size in px.
            borderRadius (int): Rounded corner radius.
            outlineWeight (int): Thickness of the outline card.
            outlineColor (str): Color of the outline card.

        Returns:
            tuple: (QFrame, QPlainTextEdit)
                - QFrame: The rounded card (outline).
                - QPlainTextEdit: The text area on top.
        """
        # Create the card frame to simulate the outline
        card = QFrame(parent)
        border_css = f"{outlineWeight}px solid {outlineColor}" if outlineWeight and outlineColor else "none"
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: {border_css};
            }}
        """)

        # Create the plain text area
        textArea = QPlainTextEdit(parent)
        textArea.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {backgroundColor};
                color: {fontColor};
                font-family: 'Lato';
                font-size: {fontSize}px;
                border-radius: {borderRadius}px;
                border: none;
                padding: 10px;
            }}
        """)
        textArea.setFont(QFont("Lato", fontSize))

        # Ensure text area is on top of the card
        textArea.raise_()

        # Return both so caller can set geometry individually
        return card, textArea

    # -----------------------------------------------------------
    # BUTTON FACTORY
    # -----------------------------------------------------------

    @staticmethod
    def createPrimaryButton(
            text, parent, backgroundColor="#0cc0df", fontColor="white",
            fontWeight=600, fontSize=12, borderRadius=10,
            outlineWeight=0, outlineColor=None
    ) -> QPushButton :
        """
        Creates a styled QPushButton with hover and click effects,
        using colors that complement the base color #0cc0df.

        Parameters:
            text (str): Button label.
            parent (QWidget): Parent widget.
            backgroundColor (str): Base background color.
            fontColor (str): Button text color.
            fontWeight (int): Font weight.
            fontSize (int): Font size in px.
            borderRadius (int): Rounded corner radius.
            outlineWeight (int): Border width.
            outlineColor (str): Border color.

        Returns:
            QPushButton: The styled button.
        """
        button = QPushButton(text, parent)
        border_css = f"{outlineWeight}px solid {outlineColor}" if outlineWeight and outlineColor else "none"

        # Complementary hover and pressed colors for #0cc0df
        hoverColor = "#26d6ec"  # slightly lighter
        pressedColor = "#0aaabf"  # slightly darker

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {backgroundColor};
                color: {fontColor};
                font-weight: {fontWeight};
                font-family: 'Lato';
                font-size: {fontSize}px;
                border-radius: {borderRadius}px;
                border: {border_css};
            }}
            QPushButton:hover {{
                background-color: {hoverColor};
            }}
            QPushButton:pressed {{
                background-color: {pressedColor};
            }}
        """)

        button.setFont(QFont("Lato", fontSize))
        return button

    @staticmethod
    def createSecondaryButton(
            text, parent, backgroundColor="#e7f9fc", fontColor="#1a1a1a",
            fontWeight=600, fontSize=12, borderRadius=10,
            outlineWeight=2, outlineColor="#185777"
    ) -> QPushButton:
        """
        Creates a styled secondary QPushButton with hover and click effects,
        using a light background with border for secondary actions.

        Parameters:
            text (str): Button label.
            parent (QWidget): Parent widget.
            backgroundColor (str): Base background color.
            fontColor (str): Button text color.
            fontWeight (int): Font weight.
            fontSize (int): Font size in px.
            borderRadius (int): Rounded corner radius.
            outlineWeight (int): Border width.
            outlineColor (str): Border color.

        Returns:
            QPushButton: The styled button.
        """
        button = QPushButton(text, parent)
        border_css = f"{outlineWeight}px solid {outlineColor}" if outlineWeight and outlineColor else "none"

        # Complementary hover and pressed colors for #e7f9fc (light cyan)
        hoverColor = "#cef2f9"  # slightly darker (main card color)
        pressedColor = "#b8e6f0"  # even darker

        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {backgroundColor};
                color: {fontColor};
                font-weight: {fontWeight};
                font-family: 'Lato';
                font-size: {fontSize}px;
                border-radius: {borderRadius}px;
                border: {border_css};
            }}
            QPushButton:hover {{
                background-color: {hoverColor};
                border: {border_css};
            }}
            QPushButton:pressed {{
                background-color: {pressedColor};
                border: {border_css};
            }}
        """)

        button.setFont(QFont("Lato", fontSize))
        return button

    # -----------------------------------------------------------
    # SHAPES / CARDS
    # -----------------------------------------------------------

    @staticmethod
    def createRoundedCard(parentClass, width=None, length=None):
        """
        Creates a rounded QFrame card with a shadow effect, commonly used for panels or KPI widgets.

        Parameters:
            parentClass (QWidget): Parent container.
            width (int): Width of the card.
            length (int): Height of the card.

        Returns:
            QFrame: The styled rounded card with shadow.
        """
        roundedCard = QFrame(parentClass)

        if width and length:
            roundedCard.setFixedSize(width, length)

        # Apply rounded card style
        roundedCard.setStyleSheet("""
            QFrame {
                background-color: #cef2f9;
                border-radius: 30px;
            }
        """)

        # Create and apply shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(40)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 80))
        roundedCard.setGraphicsEffect(shadow)

        return roundedCard

    # -----------------------------------------------------------
    # IMAGE UTILITIES
    # -----------------------------------------------------------

    @staticmethod
    def setImage(parent, imageFilePath):
        """
        Loads an image into a QLabel. The image automatically scales
        to fit its geometry.

        Parameters:
            parent (QWidget): Parent widget.
            imageFilePath (str): Path to the PNG/JPG file.

        Returns:
            QLabel: The image container.
        """
        image = QLabel(parent)
        image.setScaledContents(True)

        pixmap = QPixmap(imageFilePath)
        if pixmap.isNull():
            print(f"IMAGE FAILED TO LOAD: {imageFilePath}")
        else:
            image.setPixmap(pixmap)

        return image

    # -----------------------------------------------------------
    # PROJECT-SPECIFIC ASSETS
    # -----------------------------------------------------------

    @staticmethod
    def setBackground(parent):
        """
        Loads the MEDISYNC background image and sets its default geometry.

        Returns:
            QLabel: The background image widget.
        """
        background = Designer.setImage(parent, "../ImageResources/MEDISYNCBackground.png")
        background.setGeometry(0, 0, 1500, 800)
        return background

    @staticmethod
    def setLogo(parent):
        """
        Loads the MEDISYNC logo image.

        Returns:
            QLabel: The logo image widget.
        """
        return Designer.setImage(parent, "../ImageResources/MEDISYNCLogoBGRemoved.png")

    # -----------------------------------------------------------
    # MENU OPTIONS
    # -----------------------------------------------------------

    @staticmethod
    def createClickedOption(parent, name, imageFilePath, width):
        """
        Creates a highlighted menu option (active state) with click animation.

        Parameters:
            parent (QWidget): Parent container.
            name (str): Menu label text.
            imageFilePath (str): Icon file path.
            width (int): Width of the option frame.

        Returns:
            QFrame: Styled clickable menu option.
        """
        frame = QFrame(parent)
        frame.setStyleSheet("""
            QFrame {
                background-color: #0cc0df;  /* Base active color */
                border-radius: 20px;
            }
        """)
        frame.resize(width, 40)

        # Add label and icon
        Designer.createLabel(name, frame, "#185777", 700, 14).setGeometry(60, 10, 90, 20)
        Designer.setImage(frame, imageFilePath).setGeometry(25, 10, 20, 20)

        return frame

    @staticmethod
    def createMenuOption(parent, name, imageFilePath, width):
        """
        Creates a regular (non-active) menu option with hover and click effects.

        Parameters:
            parent (QWidget): Parent container.
            name (str): Menu label text.
            imageFilePath (str): Icon file path.
            width (int): Width of the option frame.

        Returns:
            QFrame: Styled menu option.
        """
        frame = QFrame(parent)
        baseColor = "#cef2f9"
        hoverColor = "#a3e2f5"
        pressedColor = "#8dd9ed"

        frame.setStyleSheet(f"""
            QFrame {{
                background-color: {baseColor};
                border-radius: 20px;
            }}
        """)
        frame.resize(width, 40)

        # Add label and icon
        Designer.createLabel(name, frame, "#185777", 700, 14).setGeometry(60, 10, 90, 20)
        Designer.setImage(frame, imageFilePath).setGeometry(25, 10, 20, 20)

        # -----------------------
        # Hover / Click Events
        # -----------------------
        def enterEvent(event):
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {hoverColor};
                    border-radius: 20px;
                }}
            """)
            super(QFrame, frame).enterEvent(event)

        def leaveEvent(event):
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {baseColor};
                    border-radius: 20px;
                }}
            """)
            super(QFrame, frame).leaveEvent(event)

        def mousePressEvent(event):
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {pressedColor};
                    border-radius: 20px;
                }}
            """)
            super(QFrame, frame).mousePressEvent(event)

        def mouseReleaseEvent(event):
            frame.setStyleSheet(f"""
                QFrame {{
                    background-color: {hoverColor};
                    border-radius: 20px;
                }}
            """)
            super(QFrame, frame).mouseReleaseEvent(event)

        # Assign events safely
        frame.enterEvent = enterEvent
        frame.leaveEvent = leaveEvent
        frame.mousePressEvent = mousePressEvent
        frame.mouseReleaseEvent = mouseReleaseEvent

        return frame

    # -----------------------------
    # KPI CARD
    # -----------------------------
    @staticmethod
    def createKPI(parent, iconPath, numberText, labelText,
                  width=230, height=190, x=0, y=0):
        """
        Creates a KPI (Key Performance Indicator) dashboard card
        with hover and click interaction effects.

        Parameters:
            parent (QWidget): Parent widget.
            iconPath (str): Path to the KPI icon image.
            numberText (str): Main KPI number.
            labelText (str): Description of the KPI.
            width (int): Width of the card.
            height (int): Height of the card.
            x (int): Horizontal position.
            y (int): Vertical position.

        Returns:
            QFrame: Interactive KPI widget.
        """
        # Create main card
        frame = Designer.createRoundedCard(parent, width, height)
        frame.move(x, y)

        # Base shadow for depth
        baseShadow = QGraphicsDropShadowEffect()
        baseShadow.setBlurRadius(40)
        baseShadow.setOffset(0, 6)
        baseShadow.setColor(QColor(0, 0, 0, 80))
        frame.setGraphicsEffect(baseShadow)

        # KPI Icon
        Designer.setImage(frame, iconPath).setGeometry(40, 50, 60, 60)

        # KPI Number
        Designer.createLabel(numberText, frame, "#1a1a1a", 700, 35).setGeometry(130, 60, 100, 50)

        # KPI Description
        Designer.createLabel(labelText, frame, "#333333", 400, 16).setGeometry(50, 125, 180, 40)

        # -----------------------
        # Hover effect (lift)
        # -----------------------
        def enterEvent(event):
            anim = QPropertyAnimation(frame, b"pos")
            anim.setDuration(150)
            anim.setEasingCurve(QEasingCurve.Type.OutQuad)
            anim.setStartValue(frame.pos())
            anim.setEndValue(frame.pos() - QPoint(0, 5))
            anim.start()
            frame._hover_anim = anim  # Keep reference

            baseShadow.setBlurRadius(50)
            baseShadow.setOffset(0, 8)
            super(QFrame, frame).enterEvent(event)

        def leaveEvent(event):
            anim = QPropertyAnimation(frame, b"pos")
            anim.setDuration(150)
            anim.setEasingCurve(QEasingCurve.Type.OutQuad)
            anim.setStartValue(frame.pos())
            anim.setEndValue(QPoint(x, y))
            anim.start()
            frame._hover_anim = anim

            baseShadow.setBlurRadius(40)
            baseShadow.setOffset(0, 6)
            super(QFrame, frame).leaveEvent(event)

        # -----------------------
        # Click effect
        # -----------------------
        def mousePressEvent(event):
            frame.move(frame.x(), frame.y() + 3)
            baseShadow.setBlurRadius(30)
            baseShadow.setOffset(0, 3)
            super(QFrame, frame).mousePressEvent(event)

        def mouseReleaseEvent(event):
            frame.move(frame.x(), frame.y() - 3)
            baseShadow.setBlurRadius(50 if frame.underMouse() else 40)
            baseShadow.setOffset(0, 8 if frame.underMouse() else 6)
            super(QFrame, frame).mouseReleaseEvent(event)

        # Assign events safely
        frame.enterEvent = enterEvent
        frame.leaveEvent = leaveEvent
        frame.mousePressEvent = mousePressEvent
        frame.mouseReleaseEvent = mouseReleaseEvent

        return frame

    # -----------------------------------------------------------
    # TABLE CARD
    # -----------------------------------------------------------

    @staticmethod
    def createTableCard(parentClass, labelText, fontSize,
                        columnNames, columnMap=None,
                        cardWidth=600, cardHeight=300,
                        tableWidth=None, tableHeight=None,
                        x=0, y=0,
                        data=None
                        ):
        """
        Creates a rounded card containing a label and a QTableWidget.
        Produces a clean, production-ready table card without debug output.
        """

        # Card Container
        card = Designer.createRoundedCard(parentClass, cardWidth, cardHeight)
        card.move(x, y)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 25, 20, 20)
        layout.setSpacing(10)

        # Label
        label = Designer.createLabel(labelText, card, "#1a1a1a", 700, fontSize)
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(label)

        # Table
        table = Designer.createStandardTable(columnNames)

        # Optional table size controls
        if tableWidth and tableHeight:
            table.setFixedSize(tableWidth, tableHeight)
        elif tableWidth:
            table.setFixedWidth(tableWidth)
        elif tableHeight:
            table.setFixedHeight(tableHeight)

        layout.addWidget(table)

        # Populate table
        if data:
            table.setRowCount(len(data))

            for rowIndex, row in enumerate(data):
                for colIndex, colName in enumerate(columnNames):

                    if columnMap and colName in columnMap:
                        mapper = columnMap[colName]

                        if callable(mapper):
                            value = str(mapper(row))
                        else:
                            value = str(row.get(mapper, ""))
                    else:
                        # Try direct column name
                        value = str(row.get(colName, ""))

                    item = QTableWidgetItem(value)
                    table.setItem(rowIndex, colIndex, item)

        return table, card

    @staticmethod
    def createStandardTable(columnNames):
        """
        Creates a clean, standard QTableWidget.
        Table background stays white.
        Only headers match the project theme.

        Returns:
            QTableWidget
        """
        table = QTableWidget()
        table.setColumnCount(len(columnNames))
        table.setHorizontalHeaderLabels(columnNames)

        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Standard white table, theme-colored headers
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #1a1a1a;
                font: 10px 'Lato';
                gridline-color: #d0d0d0;
                border: 2px solid #185777;
                border-radius: 5px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #b8e6f7;
                color: #185777;
                font-weight: bold;
            }
            QTableWidget::item:focus {
                background-color: #b8e6f7;
                color: #185777;
            }
            QTableWidget::item:hover {
                background-color: #e0f7fa;
            }
            QHeaderView::section {
                background-color: #0cc0df;
                color: #1a1a1a;
                font: 11px 'Lato';
                font-weight: bold;
                border: 1px solid #0aaabf;
                padding: 6px;
            }
        """)

        return table

    # -----------------------------------------------------------
    # STYLE HELPERS
    # -----------------------------------------------------------

    @staticmethod
    def applyRoundedStyle(widget, radius=10, borderColor="#185777", borderWidth=2, padding=6):
        """
        Applies a rounded border style to typical input widgets (QLineEdit, QComboBox, QDateEdit, QTextEdit).

        Parameters:
            widget (QWidget): The widget instance to style (style applied via setStyleSheet).
            radius (int): Border radius in px.
            borderColor (str): Border color hex.
            borderWidth (int): Border thickness in px.
            padding (int): Inner padding in px.
        """
        # Generic style template; for complex widgets (combo/date) additional QSS may be needed
        qss = f"""
            border: {borderWidth}px solid {borderColor};
            border-radius: {radius}px;
            padding: {padding}px;
        """
        # Append to existing style if any, but simplest is to set a prefixed QSS depending on type
        if hasattr(widget, "setStyleSheet"):
            # Distinguish types to set a minimal but safe stylesheet
            if isinstance(widget, QLineEdit):
                base = f"""
                    QLineEdit {{
                        background-color: white;
                        color: #333333;
                        font-family: 'Lato';
                        font-size: 14px;
                        {qss}
                    }}
                """
            elif isinstance(widget, QTextEdit):
                base = f"""
                    QTextEdit {{
                        background-color: white;
                        color: #333333;
                        font-family: 'Lato';
                        font-size: 14px;
                        {qss}
                    }}
                """
            elif isinstance(widget, QComboBox):
                base = f"""
                    QComboBox {{
                        background-color: white;
                        color: #333333;
                        font-family: 'Lato';
                        font-size: 14px;
                        {qss}
                        padding-right: 30px;
                    }}
                    QComboBox::drop-down {{
                        width: 30px;
                        border-left: 1px solid {borderColor};
                    }}
                """
            elif isinstance(widget, QDateEdit):
                base = f"""
                    QDateEdit {{
                        background-color: white;
                        color: #333333;
                        font-family: 'Lato';
                        font-size: 14px;
                        {qss}
                        padding-right: 30px;
                    }}
                    QDateEdit::drop-down {{
                        width: 30px;
                        border-left: 1px solid {borderColor};
                    }}
                """
            else:
                # Generic fallback
                base = f"""
                    QWidget {{
                        {qss}
                    }}
                """
            widget.setStyleSheet(base)
        else:
            # If widget doesn't support stylesheet, silently skip
            return

    @staticmethod
    def createComboBox(parent, radius=10, borderColor="#185777", fontSize=14):
        """
        Creates a styled QComboBox using the system theme with rounded corners.

        Parameters:
            parent (QWidget): Parent widget.
            radius (int): Border radius.
            borderColor (str): Border color hex.
            fontSize (int): Font size in px.

        Returns:
            QComboBox: The styled combo box ready to be positioned.
        """
        combo = QComboBox(parent)
        combo.setStyleSheet(f"""
            QComboBox {{
                background-color: white;
                color: #333333;
                font-family: 'Lato';
                font-size: {fontSize}px;
                border: 2px solid {borderColor};
                border-radius: {radius}px;
                padding: 6px;
                padding-right: 30px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 32px;
                border-left: 1px solid {borderColor};
                border-top-right-radius: {radius}px;
                border-bottom-right-radius: {radius}px;
            }}
            QComboBox QAbstractItemView {{
                color: #185777;
                background-color: white;
                selection-background-color: #2563EB;
                selection-color: white;
                }}
            """)
        return combo

    @staticmethod
    def createDateEdit(parent, radius=10, borderColor="#185777", fontSize=14):
        """
        Creates a styled QDateEdit with popup calendar and system colors.

        Parameters:
            parent (QWidget): Parent widget.
            radius (int): Border radius.
            borderColor (str): Border color.
            fontSize (int): Font size in px.

        Returns:
            QDateEdit: The styled date edit.
        """
        date = QDateEdit(parent)
        date.setCalendarPopup(True)
        date.setDate(QDate.currentDate())

        date.setStyleSheet(f"""
            QDateEdit {{
                background-color: white;
                color: #333333;
                font-family: 'Lato';
                font-size: {fontSize}px;
                border: 2px solid {borderColor};
                border-radius: {radius}px;
                padding: 6px;
                padding-right: 30px;
            }}
            QDateEdit::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 32px;
                border-left: 1px solid {borderColor};
                border-top-right-radius: {radius}px;
                border-bottom-right-radius: {radius}px;
            }}
            QCalendarWidget QWidget {{
                background-color: white;
                color: #1a1a1a;
            }}
            QCalendarWidget QTableView {{
                background-color: white;
                selection-background-color: #0cc0df;
                selection-color: white;
            }}
            QCalendarWidget QToolButton {{
                color: white;
                background-color: #0cc0df;
            }}
            QCalendarWidget QMenu {{
                background-color: white;
                color: #1a1a1a;
            }}
            QCalendarWidget QSpinBox {{
                background-color: white;
                color: #1a1a1a;
            }}
        """)
        return date